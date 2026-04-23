import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)  # начинаем с 0% заполнения (0 В)
        if self.verbose:
            print(f"PWM_DAC инициализирован: пин {self.gpio_pin}, частота {self.pwm_frequency} Гц, диапазон {self.dynamic_range} В")

    def deinit(self):
        self.pwm.stop()
        GPIO.cleanup(self.gpio_pin)
        if self.verbose:
            print("PWM_DAC деинициализирован, ШИМ остановлен")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.2f} В выходит за диапазон (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            duty_cycle = 0
        else:
            duty_cycle = (voltage / self.dynamic_range) * 100
        self.pwm.ChangeDutyCycle(duty_cycle)
        if self.verbose:
            print(f"Установлено напряжение ~{voltage:.2f} В (коэффициент заполнения {duty_cycle:.1f}%)")

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.290, True)   # пин 12, частота 500 Гц, опорное ~3.29 В
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    finally:
        dac.deinit()