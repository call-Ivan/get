import r2r_dac as r2r
import signal_generator as sg
import time

if __name__ == "__main__":
    amplitude = 3.2          # амплитуда синусоиды (В)
    signal_frequency = 10    # частота сигнала (Гц)
    sampling_frequency = 1000 # частота дискретизации (Гц)

    dac_pins = [16, 20, 21, 25, 26, 17, 27, 22]
    dynamic_range = 3.3

    try:
        dac = r2r.R2R_DAC(dac_pins, dynamic_range, verbose=False)
        print(f"Генерация синусоиды: амплитуда={amplitude} В, частота={signal_frequency} Гц, дискретизация={sampling_frequency} Гц")
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