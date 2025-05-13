import numpy as np
from ruckig import Ruckig, InputParameter, Result
import matplotlib.pyplot as plt

# DOF 및 관절 제한 정의
DOF = 4
max_vel = [1.0, 1.0, 1.0, 1.0] # rad/s
max_acc = [1.0, 1.0, 1.0, 1.0] # rad/s^2
lower_limit = [-1.0, -1.0, -1.0, -1.0]
upper_limit = [1.0, 1.0, 1.0, 1.0]

# Ruckig 인스턴스 생성성
otg = Ruckig(
    degrees_of_freedom=DOF,
    max_velocity=max_vel,
    max_acceleration=max_acc,
    min_position=lower_limit,
    max_position=upper_limit
)

# 파라미터
inp = InputParameter(DOF)
inp.current_position = [0.0, 0.0, 0.0, 0.0]
inp.current_velocity = [0.0] * DOF
inp.current_acceleration = [0.0] * DOF

inp.target_position = [0.5, 0.5, 0.5, 0.5]
inp.target_velocity = [0.0] * DOF
inp.target_acceleration = [0.0] * DOF

# 궤적 계산
res = Result()
trajectory = []

while True:
    status = otg.update(inp, res)
    trajectory.append({
        "position": res.new_position.copy(),
        "velocity": res.new_velocity.copy(),
        "acceleration": res.new_acceleration.copy(),
    })

    # 다음 스텝 위한 현재 상태 갱신
    inp.current_position = res.new_position
    inp.current_velocity = res.new_velocity
    inp.current_acceleration = res.new_acceleration
    if status != Result.Working:
        break

# 궤적 시각화
def plot_trajectory(trajectory):
    time_steps = len(trajectory)
    time = np.linspace(0, time_steps, time_steps)

    for i in range(DOF):
        positions = [step["position"][i] for step in trajectory]
        velocities = [step["velocity"][i] for step in trajectory]
        accelerations = [step["acceleration"][i] for step in trajectory]

        plt.figure(figsize=(12, 8))
        plt.subplot(3, 1, 1)
        plt.plot(time, positions, label=f'Position {i+1}')
        plt.legend()
        plt.subplot(3, 1, 2)
        plt.plot(time, velocities, label=f'Velocity {i+1}')
        plt.legend()
        plt.subplot(3, 1, 3)
        plt.plot(time, accelerations, label=f'Acceleration {i+1}')
        plt.legend()
        plt.tight_layout()
        plt.show()