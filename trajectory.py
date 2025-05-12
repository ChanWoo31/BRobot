import numpy as np

def lspb_segment(q0, q1, V_max, A_max, N=100):
    dq = q1 - q0
    T_a = V_max / A_max
    # 등속 구간 길이 계산
    T_flat = (dq - A_max*T_a**2) / V_max
    # 전체 구간 시간
    T = 2*T_a + T_flat
    # 시간 샘플
    t = np.linspace(0, T, N)
    q = np.zeros_like(t)
    for i, ti in enumerate(t):
        if ti < T_a:
            q[i] = q0 + 0.5*A_max*ti**2
        elif ti < (T - T_a):
            q[i] = q0 + 0.5*A_max*T_a**2 + V_max*(ti - T_a)
        else:
            dt = T - ti
            q[i] = q1 - 0.5*A_max*dt**2
    return t, q

# 예시: 하나의 관절에 대해
q0, q1 = 0.0, 1.0         # 시작/끝 각도 [rad]
V_max, A_max = 0.5, 1.0   # rad/s, rad/s²
t, q = lspb_segment(q0, q1, V_max, A_max)

