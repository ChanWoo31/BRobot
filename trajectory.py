import numpy as np
from ruckig import Ruckig, InputParameter, OutputParameter, Result
import matplotlib.pyplot as plt

# 1) DOF 및 타임스텝 정의
DOF = 4
dt  = 0.01  # 제어 주기(초)

# 2) Ruckig 인스턴스 생성
otg = Ruckig(DOF, dt)

# 3) InputParameter 세팅
inp = InputParameter(DOF)
inp.min_position     = [-1.0]*DOF
inp.max_position     = [ 1.0]*DOF
inp.max_velocity     = [1.0]*DOF
inp.max_acceleration = [1.0]*DOF

inp.current_position     = [0.0]*DOF
inp.current_velocity     = [0.0]*DOF
inp.current_acceleration = [0.0]*DOF

inp.target_position      = [0.5]*DOF
inp.target_velocity      = [0.0]*DOF
inp.target_acceleration  = [0.0]*DOF

# 4) OutputParameter 생성 (여기가 핵심 수정점)
out = OutputParameter(DOF)

# 5) 궤적 생성 및 수집
positions = []
times = []
t = 0.0

while True:
    status = otg.update(inp, out)    # inp, out을 넘겨 줌
    positions.append(out.new_position.copy())
    times.append(t)
    t += dt

    # 다음 스텝을 위해 inp에 최신 상태 복사
    out.pass_to_input(inp)

    if status != Result.Working:
        break

positions = np.array(positions)
times = np.array(times)

# 6) 플롯
for i in range(DOF):
    plt.figure()
    plt.plot(times, positions[:, i], label=f'Joint {i+1}')
    plt.title(f'Joint {i+1} Position vs Time')
    plt.xlabel('Time [s]')
    plt.ylabel('Position [rad]')
    plt.legend()
    plt.tight_layout()

plt.show()
