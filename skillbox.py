import numpy as np
from sympy import symbols, Sum, Matrix

class MathModelQuadrotor:
    def __init__(self, m, R, Pi, g, omega_bx, omega_by, omega_bz, Ixx, Iyy, Izz):
        self.m = m
        self.R = R
        self.Pi = Pi
        self.g = g
        self.omega_bx = omega_bx
        self.omega_by = omega_by
        self.omega_bz = omega_bz
        self.Ixx = Ixx
        self.Iyy = Iyy
        self.Izz = Izz

        # Параметры ПИД-регулятора
        self.Kp_roll = 1.0
        self.Ki_roll = 0.1
        self.Kd_roll = 0.01
        self.Kp_pitch = 1.0
        self.Ki_pitch = 0.1
        self.Kd_pitch = 0.01
        self.Kp_yaw = 1.0
        self.Ki_yaw = 0.1
        self.Kd_yaw = 0.01
        self.Kp_height = 1.0
        self.Ki_height = 0.1
        self.Kd_height = 0.01

        # Переменные для хранения предыдущих ошибок ПИД-регулятора
        self.prev_error_roll = 0
        self.prev_error_pitch = 0
        self.prev_error_yaw = 0
        self.prev_error_height = 0

    def compute_control_signal(self, target_roll, target_pitch, target_yaw, target_height,
                               current_roll, current_pitch, current_yaw, current_height, dt):
        # Вычисление ошибок
        error_roll = target_roll - current_roll
        error_pitch = target_pitch - current_pitch
        error_yaw = target_yaw - current_yaw
        error_height = target_height - current_height

        # Вычисление компонент ПИД-регулятора
        pid_roll = self.Kp_roll * error_roll + self.Ki_roll * self.prev_error_roll * dt + self.Kd_roll * (error_roll - self.prev_error_roll) / dt
        pid_pitch = self.Kp_pitch * error_pitch + self.Ki_pitch * self.prev_error_pitch * dt + self.Kd_pitch * (error_pitch - self.prev_error_pitch) / dt
        pid_yaw = self.Kp_yaw * error_yaw + self.Ki_yaw * self.prev_error_yaw * dt + self.Kd_yaw * (error_yaw - self.prev_error_yaw) / dt
        pid_height = self.Kp_height * error_height + self.Ki_height * self.prev_error_height * dt + self.Kd_height * (error_height - self.prev_error_height) / dt

        # Обновление предыдущих ошибок
        self.prev_error_roll = error_roll
        self.prev_error_pitch = error_pitch
        self.prev_error_yaw = error_yaw
        self.prev_error_height = error_height

        # Вычисление матрицы по первой формуле
        n = len(self.Pi)
        i, n = symbols('i n')
        first_matrix = np.array([[0, 0, Sum(self.Pi, (i, 1, n))]])
        second_matrix = np.array([0, 0, -self.g])
        total_matrix = 1 / self.m * self.R * first_matrix + second_matrix

        # Вычисление матрицы по второй формуле
        omega_0, omega_1, omega_2, omega_3 = symbols('omega_0 omega_1 omega_2 omega_3')
        i_b0, i_b1, i_b2, i_b3 = symbols('i_b0 i_b1 i_b2 i_b3')
        d = symbols('d')
        matrix_I = np.array([[self.Ixx, 0, 0], [0, self.Iyy, 0], [0, 0, self.Izz]])
        omega_matrix = np.array([self.omega_bx, self.omega_by, self.omega_bz])

        matrix_expr = Matrix([
            [i_b0 * (omega_0**2 - omega_2**2)],
            [i_b1 * (omega_3**2 - omega_1**2)],
            [d * (omega_3**2 + omega_1**2 - omega_0**2 - omega_2**2)]
        ])

        second_total_matrix = np.linalg.inv(matrix_I).dot(matrix_expr - omega_matrix * (matrix_I.dot(omega_matrix)))

        return total_matrix, second_total_matrix, pid_roll, pid_pitch, pid_yaw, pid_height

# Пример использования класса
quadrotor = MathModelQuadrotor(m=1.0, R=1.0, Pi=[1.0, 1.0, 1.0, 1.0], g=9.81,
                               omega_bx=0.0, omega_by=0.0, omega_bz=0.0,
                               Ixx=1.0, Iyy=1.0, Izz=1.0)

# Установка желаемых углов и высоты
target_roll, target_pitch, target_yaw, target_height = 0.0, 0.0, 0.0, 1.0

# Установка текущих углов и высоты
current_roll, current_pitch, current_yaw, current_height = 0.0, 0.0, 0.0, 0.0

# Шаг времени
dt = 0.01

# Вычисление управляющих сигналов
total_matrix, second_total_matrix, pid_roll, pid_pitch, pid_yaw, pid_height = quadrotor.compute_control_signal(
    target_roll, target_pitch, target_yaw, target_height, current_roll, current_pitch, current_yaw, current_height, dt)

# Вывод управляющих сигналов
print("Total Matrix (Formula 1):", total_matrix)
print("Second Total Matrix (Formula 2):", second_total_matrix)
print("Roll Control:", pid_roll)
print("Pitch Control:", pid_pitch)
print("Yaw Control:", pid_yaw)
print("Height Control:", pid_height)
