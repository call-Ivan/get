import r2r_adc as adc
import time
import adc_plot

# --- Настройки измерений ---
# Динамический диапазон (опорное напряжение) — ИЗМЕРЬТЕ МУЛЬТИМЕТРОМ!
DYNAMIC_RANGE = 3.30    # <-- ПОДСТАВЬТЕ ВАШЕ РЕАЛЬНОЕ ЗНАЧЕНИЕ
# Продолжительность измерений (в секундах)
DURATION = 3.0

# --- Создание объекта АЦП ---
# compare_time = 0.0001 с (100 мкс) — как указано в инструкции
adc_device = adc.R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=0.0001, verbose=False)

# --- Списки для данных ---
voltage_values = []   # список для хранения напряжений
time_values = []      # список для хранения моментов времени

try:
    # Сохраняем момент начала эксперимента
    start_time = time.time()
    
    print(f"Начало измерений. Продолжительность: {DURATION} с")
    print(f"Динамический диапазон: {DYNAMIC_RANGE} В")
    print("Измеряю...")
    
    # Пока разница между текущим временем и начальным меньше DURATION
    while (time.time() - start_time) < DURATION:
        # Измеряем напряжение
        voltage = adc_device.get_sc_voltage()
        # Текущий момент времени (относительно старта)
        current_time = time.time() - start_time
        
        # Добавляем в списки
        voltage_values.append(voltage)
        time_values.append(current_time)
    
    print(f"Измерения завершены. Получено {len(voltage_values)} точек.")
    print("Строим график...")
    
    # Отображаем график
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)

except KeyboardInterrupt:
    print("\nПрерывание пользователем")
finally:
    # Вызываем деструктор (очистка GPIO)
    adc_device.deinit()
    print("Ресурсы GPIO освобождены")
