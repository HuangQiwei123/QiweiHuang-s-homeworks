"""
水库多目标优化调度 — 独立实现
================================
基于 Experiment 3 实验文档, 使用 scipy.optimize 求解 7 天最优放水方案。
目标: 最大化水力发电收益, 最小化生态亏欠。
约束: 库容边界、放水边界、水量平衡。
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import numpy as np
from scipy.optimize import minimize, Bounds, NonlinearConstraint
import matplotlib.pyplot as plt

# ============================================================
# 水库运行参数 (来自实验文档)
# ============================================================
V0      = 500_000          # 初始库容 (m3)
V_min   = 100_000          # 最小库容 (m3)
V_max   = 1_000_000        # 最大库容 (m3)
Q_eco   = 10.0             # 最小生态放水量 (m3/s)
Q_max   = 100.0            # 最大放水量 (m3/s)
DT      = 86_400           # 日秒数 (s)
T       = 7                # 决策周期 (天)

# 7 天预测数据
inflow  = np.array([15, 12, 10, 8, 12, 15, 18], dtype=float)   # 入库流量 (m3/s)
price   = np.array([0.08, 0.08, 0.08, 0.08, 0.10, 0.12, 0.10]) # 电价 ($/kWh)

# 水力发电转换系数
#   功率 P_hydro (kW) = eta * rho * g * H * Q / 1000
#   日发电量 (kWh)    = P_hydro * 24
#   合并: K * Q,  其中 K = eta * rho * g * H * 24 / 1000  (kWh per m3/s per day)
ETA     = 0.90            # 水轮机效率
RHO     = 1000.0          # 水密度 (kg/m3)
G       = 9.81            # 重力加速度 (m/s2)
HEAD    = 50.0            # 发电水头 (m)

K_HYDRO = ETA * RHO * G * HEAD * 24 / 1000   # kWh/(m3/s)/day


# ============================================================
# 基础函数
# ============================================================
def storage_trajectory(Q):
    """水量平衡: 由放水序列 Q[0..6] 返回每日末库容 S[0..6] (m3)."""
    S = np.empty(T)
    cur = V0
    for t in range(T):
        cur += (inflow[t] - Q[t]) * DT
        S[t] = cur
    return S


def hydropower_revenue(Q):
    """总发电收益 ($)."""
    return K_HYDRO * np.dot(Q, price)


def ecological_deficit(Q):
    """生态亏欠: sum(max(0, Q_eco - Q_t)) (m3/s)."""
    return np.sum(np.maximum(0.0, Q_eco - Q))


# ============================================================
# 约束构建
# ============================================================
def make_constraints():
    """构造库容不等式约束 (NonlinearConstraint 格式)."""
    def c_upper(Q):
        return V_max - storage_trajectory(Q)   # >= 0 即 V <= V_max

    def c_lower(Q):
        return storage_trajectory(Q) - V_min    # >= 0 即 V >= V_min

    return [
        NonlinearConstraint(c_upper, 0.0, np.inf),
        NonlinearConstraint(c_lower, 0.0, np.inf),
    ]


# ============================================================
# 单目标优化
# ============================================================
def optimize_hard_eco():
    """硬生态约束: Q_t >= Q_eco, 最大化收益."""
    bounds = Bounds([Q_eco] * T, [Q_max] * T)
    cons = make_constraints()

    def objective(Q):
        return -hydropower_revenue(Q)

    # 多起点尝试
    x0_list = [
        np.full(T, 15.0),
        np.full(T, 20.0),
        np.clip(inflow, Q_eco + 1, Q_max - 1),
        np.full(T, Q_eco + 5.0),
    ]
    best = None
    for x0 in x0_list:
        res = minimize(objective, x0, method='SLSQP', bounds=bounds,
                       constraints=cons, options={'maxiter': 2000, 'ftol': 1e-12})
        if best is None or res.fun < best.fun:
            best = res
    return best


def optimize_no_eco():
    """无生态下限: Q_t >= 0, 最大化收益."""
    bounds = Bounds([0.0] * T, [Q_max] * T)
    cons = make_constraints()

    def objective(Q):
        return -hydropower_revenue(Q)

    x0_list = [
        np.full(T, 15.0),
        np.full(T, 20.0),
        np.clip(inflow, 1.0, Q_max - 1),
    ]
    best = None
    for x0 in x0_list:
        res = minimize(objective, x0, method='SLSQP', bounds=bounds,
                       constraints=cons, options={'maxiter': 2000, 'ftol': 1e-12})
        if best is None or res.fun < best.fun:
            best = res
    return best


# ============================================================
# 多目标 — 加权和法
# ============================================================
def optimize_weighted(alpha):
    """
    加权目标: minimize  -alpha * revenue_norm + (1-alpha) * deficit_norm
    alpha = 0 → 纯生态,  alpha = 1 → 纯收益.
    使用归一化避免量纲问题.
    """
    rev_scale = K_HYDRO * Q_max * np.sum(price)         # 收益上界 (不可能达到)
    def_scale = Q_eco * T                                 # 亏欠上界

    bounds = Bounds([0.0] * T, [Q_max] * T)
    cons = make_constraints()

    def objective(Q):
        rev_norm = hydropower_revenue(Q) / rev_scale
        def_norm = ecological_deficit(Q) / def_scale
        return -alpha * rev_norm + (1.0 - alpha) * def_norm

    # 多起点
    x0_list = [
        np.clip(inflow, 0.0, Q_max),
        np.full(T, Q_eco + 2.0),
        np.full(T, 15.0),
    ]
    best_res, best_obj = None, np.inf
    for x0 in x0_list:
        res = minimize(objective, x0, method='SLSQP', bounds=bounds,
                       constraints=cons, options={'ftol': 1e-9, 'maxiter': 2000})
        S = storage_trajectory(res.x)
        feasible = np.all((S >= V_min - 100.0) & (S <= V_max + 100.0))
        if feasible and res.fun < best_obj:
            best_obj = res.fun
            best_res = res
    return best_res if best_res is not None else res


def compute_pareto_frontier(n=30):
    """生成帕累托前沿点集."""
    points = []
    alphas = np.linspace(0.0, 1.0, n)

    for a in alphas:
        res = optimize_weighted(a)
        Q = res.x
        S = storage_trajectory(Q)
        if np.all((S >= V_min - 100.0) & (S <= V_max + 100.0)):
            points.append((ecological_deficit(Q), hydropower_revenue(Q), a))

    points.sort(key=lambda p: p[0])
    pts = np.array(points)

    print(f"  帕累托端点 — 纯收益: ${pts[-1,1]:,.2f}  (亏欠 {pts[-1,0]:.2f})")
    print(f"  帕累托端点 — 纯生态: ${pts[0,1]:,.2f}   (亏欠 {pts[0,0]:.4f})")
    return pts


# ============================================================
# 验证
# ============================================================
def verify(Q, label="方案"):
    """验证约束满足情况并打印报告."""
    S = storage_trajectory(Q)
    eps_v = 100.0    # 库容容差 (m3), 0.1% of V_min
    eps_b = 1.0      # 水量平衡容差 (m3)

    # 1. 放水边界
    r_pass = int(np.all(Q >= Q_eco - 1e-9) and np.all(Q <= Q_max + 1e-9))
    r_eco_violations = int(np.sum(Q < Q_eco - 0.01))

    # 2. 库容边界
    v_lo_ok = np.all(S >= V_min - eps_v)
    v_hi_ok = np.all(S <= V_max + eps_v)

    # 3. 水量平衡
    mass_err = 0.0
    cur = V0
    for t in range(T):
        expected = cur + (inflow[t] - Q[t]) * DT
        err = abs(S[t] - expected)
        mass_err = max(mass_err, err)
        cur = S[t]
    mass_ok = mass_err < eps_b

    # 4. 收益
    rev = hydropower_revenue(Q)

    all_ok = r_pass and v_lo_ok and v_hi_ok and mass_ok

    print(f"\n{'='*60}")
    print(f"  验证报告: {label}")
    print(f"{'='*60}")
    print(f"  {'检验项':<28} {'判定':>8}")
    print(f"  {'-'*38}")
    print(f"  {'放水边界 [10, 100] m3/s':<28} {'PASS' if r_pass else 'FAIL':>8}")
    print(f"  {'库容 >= 100,000 m3':<28} {'PASS' if v_lo_ok else 'FAIL':>8}")
    print(f"  {'库容 <= 1,000,000 m3':<28} {'PASS' if v_hi_ok else 'FAIL':>8}")
    print(f"  {'水量平衡 (max err)':<28} {'PASS' if mass_ok else 'FAIL':>8}"
          f" ({mass_err:.2e} m3)")

    if r_eco_violations:
        print(f"\n  *** 生态违规 {r_eco_violations} 天:")
        for t in range(T):
            if Q[t] < Q_eco - 0.01:
                print(f"      第{t+1}天: Q={Q[t]:.2f} < {Q_eco}")

    print(f"\n  {'天':>3}  {'放水':>8}  {'入库':>8}  {'日末库容':>14}  {'生态?':>6}")
    print(f"  {'-'*46}")
    for t in range(T):
        eco_flag = "OK" if Q[t] >= Q_eco - 1e-9 else "FAIL"
        print(f"  {t+1:>3}  {Q[t]:>8.2f}  {inflow[t]:>8.1f}  {S[t]:>14,.0f}  {eco_flag:>6}")

    print(f"\n  总收益: ${rev:,.2f}")
    print(f"  终库容: {S[-1]:,.0f} m3")
    print(f"  结论: {'全部通过' if all_ok else '存在违反'}")
    print(f"{'='*60}")

    return all_ok


# ============================================================
# 绘图
# ============================================================
def plot_pareto(pts):
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 10,
        'axes.titlesize': 11,
        'axes.labelsize': 10,
        'axes.linewidth': 0.8,
        'xtick.major.width': 0.8,
        'ytick.major.width': 0.8,
        'figure.dpi': 120,
    })

    eco = pts[:, 0]
    rev = pts[:, 1] / 1000
    alpha = pts[:, 2]
    colors = plt.cm.RdYlGn(1 - alpha)
    bbox_style = dict(boxstyle='round,pad=0.4', facecolor='white',
                      edgecolor='#aaa', alpha=0.92)

    fig = plt.figure(figsize=(14, 10))

    # ================================================================
    # 图 A: 帕累托前沿 (上半)
    # ================================================================
    axA = fig.add_axes([0.07, 0.42, 0.90, 0.53])
    axA.scatter(eco, rev, c=colors, s=80, zorder=5, edgecolors='#333',
                linewidths=0.4)
    axA.plot(eco, rev, '-', color='#555', lw=1.0, alpha=0.5, zorder=3)

    # 端点标注
    axA.annotate(f'Pure Revenue  |  ${rev[-1]:.1f}k  |  deficit {eco[-1]:.1f}',
                 (eco[-1], rev[-1]), xytext=(30, -15), textcoords='offset points',
                 fontsize=8, ha='left', bbox=bbox_style,
                 arrowprops=dict(arrowstyle='->', color='#c62828', lw=1.2))
    axA.annotate(f'Eco Priority  |  ${rev[0]:.1f}k  |  deficit ~ 0',
                 (eco[0], rev[0]), xytext=(-105, 20), textcoords='offset points',
                 fontsize=8, ha='left', bbox=bbox_style,
                 arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1.2))

    # 生态成本箭头
    mid_x = (eco[0] + eco[-1]) / 2
    mid_y = (rev[0] + rev[-1]) / 2
    axA.annotate('', xy=(eco[-1], rev[-1]), xytext=(eco[0], rev[0]),
                 arrowprops=dict(arrowstyle='<->', color='#e65100',
                                 lw=1.2, ls='dashed'))
    axA.text(mid_x + 0.5, mid_y + 0.03,
             f'Cost ≈ ${rev[-1] - rev[0]:.0f}',
             fontsize=8, color='#e65100', ha='center', fontweight='bold')

    axA.set_xlabel('Ecological Deficit  (m3/s)')
    axA.set_ylabel('Hydropower Revenue  (k$)')
    axA.set_title('(a)  Pareto Frontier: Revenue vs. Ecological Deficit',
                  fontweight='bold', loc='left')
    axA.grid(True, alpha=0.25, lw=0.5)
    axA.set_xlim(left=min(-0.5, eco[0] - 0.3))
    axA.set_ylim(bottom=rev[0] - 0.4, top=rev[-1] + 0.4)

    # ================================================================
    # 图 B: 三种策略的放水调度 (左下)
    # ================================================================
    axB = fig.add_axes([0.07, 0.07, 0.42, 0.26])

    idx_mid = len(pts) // 2
    for idx, label, color, ls in [
        (0,   'Eco priority', '#2e7d32', 'solid'),
        (idx_mid, 'Balanced',  '#f9a825', 'dashed'),
        (-1,  'Pure revenue','#c62828', 'dotted'),
    ]:
        a_val = pts[idx, 2]
        res = optimize_weighted(a_val)
        Q = res.x
        axB.plot(range(1, T + 1), Q, marker='o', color=color,
                 lw=1.5, ms=5, ls=ls, label=label)

    axB.axhline(y=Q_eco, color='#555', lw=0.8, ls='--', alpha=0.6)
    axB.text(7.2, Q_eco + 0.3, f'Q_eco = {Q_eco}', fontsize=7,
             color='#555', va='bottom')
    axB.set_xlabel('Day')
    axB.set_ylabel('Release  (m3/s)')
    axB.set_title('(b)  Release Schedules at Three Operating Points',
                  fontweight='bold', loc='left')
    axB.set_xticks(range(1, T + 1))
    axB.legend(fontsize=7, loc='upper right', framealpha=0.9)
    axB.grid(True, alpha=0.25, lw=0.5)
    axB.set_xlim(0.5, 7.8)

    # ================================================================
    # 图 C: 边际替代率 (右下)
    # ================================================================
    axC = fig.add_axes([0.55, 0.07, 0.42, 0.26])

    marginal = []
    for i in range(1, len(eco)):
        de = eco[i] - eco[i - 1]
        if abs(de) > 1e-8:
            dr_k = (rev[i] - rev[i - 1]) * 1000
            marginal.append(((eco[i] + eco[i - 1]) / 2, -dr_k / de))

    if marginal:
        mc = np.array(marginal)
        axC.plot(mc[:, 0], mc[:, 1], 'o-', color='#7b1fa2',
                 ms=5, lw=1.5, label='Marginal cost')
        axC.annotate('Cheap', (mc[0, 0], mc[0, 1]),
                     xytext=(10, 15), textcoords='offset points',
                     fontsize=7, color='#333',
                     arrowprops=dict(arrowstyle='->', color='#888'))
        axC.annotate('Expensive', (mc[-1, 0], mc[-1, 1]),
                     xytext=(-50, -20), textcoords='offset points',
                     fontsize=7, color='#333',
                     arrowprops=dict(arrowstyle='->', color='#888'))

    axC.set_xlabel('Ecological Deficit  (m3/s)')
    axC.set_ylabel('Marginal Cost  ($ per m3/s)')
    axC.set_title('(c)  Marginal Cost of Eliminating Ecological Deficit',
                  fontweight='bold', loc='left')
    axC.grid(True, alpha=0.25, lw=0.5)
    axC.legend(fontsize=7)

    # 总标题
    fig.suptitle('Reservoir Dispatch — Multi-Objective Trade-off Analysis',
                 fontsize=14, fontweight='bold', y=0.98)

    fig.savefig('tradeoff_analysis.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print("\n[图表: tradeoff_analysis.png]")


# ============================================================
# 主程序
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("  水库多目标优化调度")
    print("=" * 60)

    # ---- Part 1: 核心优化 ----
    print("\n[1] 硬生态约束优化 (Q >= 10 m3/s)...")
    sol_eco = optimize_hard_eco()
    Q_eco_opt = sol_eco.x
    print(f"    总收益 = ${hydropower_revenue(Q_eco_opt):,.2f}")
    print(f"    SLSQP 迭代 = {sol_eco.nit},  成功 = {sol_eco.success}")

    # ---- Part 2: 无约束对比 ----
    print("\n[2] 无生态约束优化 (Q >= 0)...")
    sol_free = optimize_no_eco()
    Q_free = sol_free.x
    print(f"    总收益 = ${hydropower_revenue(Q_free):,.2f}")
    print(f"    生态亏欠 = {ecological_deficit(Q_free):.2f} m3/s")

    # ---- Part 3: 帕累托前沿 ----
    print("\n[3] 帕累托前沿 (30 个权重)...")
    pareto = compute_pareto_frontier(n=30)

    # ---- Part 4: 生态成本 ----
    rev_eco = hydropower_revenue(Q_eco_opt)
    rev_free = hydropower_revenue(Q_free)
    cost = rev_free - rev_eco
    print(f"\n[4] 生态成本: ${cost:,.2f}  ({cost/rev_free*100:.1f}% 的收益)")

    # ---- Part 5: 图表 ----
    plot_pareto(pareto)

    # ---- Part 6: 验证 ----
    print("\n[5] 约束验证")
    verify(Q_eco_opt, "生态硬约束最优解")
    verify(Q_free, "无生态约束最优解")

    # ---- Part 7: 导出 ----
    S_opt = storage_trajectory(Q_eco_opt)
    with open('optimal_schedule.csv', 'w') as f:
        f.write("Day,Inflow_m3s,Release_m3s,Storage_m3,Price_per_kWh,Revenue_USD\n")
        for t in range(T):
            rev_t = K_HYDRO * Q_eco_opt[t] * price[t]
            f.write(f"{t+1},{inflow[t]:.1f},{Q_eco_opt[t]:.4f},{S_opt[t]:.0f},"
                    f"{price[t]:.2f},{rev_t:.2f}\n")
    print("\n[6] optimal_schedule.csv 已导出")

    # ---- 分析文字 ----
    print(f"""
{'='*60}
  权衡分析
{'='*60}

【帕累托前沿】从纯生态(α=0)到纯收益(α=1), 前沿呈下凹形。
  越靠近零亏欠端, 每消除一单位亏欠的边际成本越高。

【生态约束的代价】维持 Q>=10 m3/s 付出约 ${cost:,.0f} 收益损失
  ({cost/rev_free*100:.1f}%)。亏损集中在低电价日(第3-4天 $0.08/kWh)
  被迫放水, 丧失了将这些水储存到第6天高价($0.12)释放的机会。

【优先生态时的调度变化】
  1. 放水更均匀, 紧贴入库流量, 库容波动减小
  2. 价格信号被压制, 高电价日的"抢发"行为减弱
  3. 从"以电定水"转为"以水定电" — 先保生态基线, 再优化收益
""")

    plt.show()
