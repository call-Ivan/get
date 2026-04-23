import numpy as np
import time

def get_sin_wave_amplitude(freq, t):
    """
    Возвращает нормализованное значение синусоиды (0..1) в момент времени t.
    Формула: (sin(2πft) + 1) / 2
    """
    return (np.sin(2 * np.pi * freq * t) + 1) / 2

def wait_for_sampling_period(sampling_frequency):
    """Задерживает выполнение на один период дискретизации."""
    time.sleep(1.0 / sampling_frequency)