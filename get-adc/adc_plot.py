import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    """
    Строит график зависимости напряжения от времени.
    
    Аргументы:
        time (list): список моментов времени (в секундах)
        voltage (list): список измеренных напряжений (в вольтах)
        max_voltage (float): максимальное значение для границ по оси Y
    """
    # Создаём окно для отображения графика (10 дюймов на 6 дюймов)
    plt.figure(figsize=(10, 6))
    
    # Размещаем график зависимости напряжения от времени
    plt.plot(time, voltage, marker='o', markersize=4, linewidth=1.5)
    
    # Задаём название графика и подписи осей
    plt.title("Зависимость напряжения на выходе ЦАП от времени", fontsize=14)
    plt.xlabel("Время, с", fontsize=12)
    plt.ylabel("Напряжение, В", fontsize=12)
    
    # Задаём границы по осям X и Y
    # X: от 0 до максимального времени в списке (с небольшим запасом)
    if time:
        plt.xlim(0, max(time) * 1.05)
    # Y: от 0 до max_voltage (с небольшим запасом 5%)
    plt.ylim(0, max_voltage * 1.05)
    
    # Включаем отображение сетки
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Отображаем график
    plt.show()
