import mcp4725_driver as mcp
import signal_generator as sg
import time

if __name__ == "__main__":
    amplitude = 3           # амплитуда синусоиды (В), не более dynamic_range
    signal_frequency = 10     # частота сигнала (Гц)
    sampling_frequency = 1000 # частота дискретизации (Гц)

    dynamic_range = 5.0       # опорное напряжение MCP4725 (В)

    try:
        dac = mcp.MCP4725(dynamic_range, address=0x61, verbose=False)
        print(f"Генерация синусоиды через MCP4725: амплитуда={amplitude} В, частота={signal_frequency} Гц, дискретизация={sampling_frequency} Гц")
        print("Нажмите Ctrl+C для остановки")

        t = 0.0
        period = 1.0 / sampling_frequency

        while True:
            coef = sg.get_sin_wave_amplitude(signal_frequency, t)
            voltage = amplitude * coef
            dac.set_voltage(voltage)
            time.sleep(period)
            t += period

    finally:
        dac.deinit()