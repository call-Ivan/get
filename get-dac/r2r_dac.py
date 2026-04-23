import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        number = max(0, min(255, number))
        for i, pin in enumerate(self.gpio_bits):
            bit = (number >> i) & 1
            GPIO.output(pin, bit)
        if self.verbose:
            print(f"Установлен код {number}")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за диапазон (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            code = 0
        else:
            code = int(voltage / self.dynamic_range * 255)
        self.set_number(code)
        if self.verbose:
            actual = code / 255 * self.dynamic_range
            print(f"Установлено напряжение ~{actual:.2f} В")

if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.3, True)
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    finally:
        dac.deinit()