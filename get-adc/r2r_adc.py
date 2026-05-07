import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose=False):
            
            self.dynamic_range = dynamic_range
            self.verbose = verbose
            self.compare_time = compare_time

            self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
            self.comp_gpio = 21

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
            GPIO.setup(self.comp_gpio, GPIO.IN)
    
    def definit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()
        if self.verbose:
            print("R2R_ADC деинициализирован")
    
    def number_to_dac(self, number):
        """Set binary number to R2R DAC"""
        number = max(0, min(255, number))
        for i, pin in enumerate(self.bits_gpio):
            bit = (number >> (7 - i)) & 1  # MSB first
            GPIO.output(pin, bit)
        if self.verbose:
            print(f"ЦАП установлен код {number}")
    
    def sequential_couting_adc(self):
        for code in range (256):
            self.number_to_dac(code)
            time.sleep(self.compare_time)

            if GPIO.input(self.comp_gpio):
                if self.verbose:
                    print(f"Компаратор сработал на коде {code}")
                return code

        if self.verbose(self):
            print("Входное напряжение выше диапазона, возвращаем 255")
        return 255
    
    def get_sc_voltage(self):

        code = self.sequential_couting_adc()
        voltage +(code/255.0) * self.dynamic_range
        if self.verbose:
            print(f"Код {code} -> напряжение {voltage:. 3f} B")
        return voltage

if __name__ == "_main_":
    DYNAMIC_RANGE = 3.30

    try:
        adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time= 0.01, verbose=True)

        print(f"Начало измерений (динамический диапазон = {DYNAMIC_RANGE} B)")
        
        while True:
            voltage = adc.get_sc_voltage()
            print(f"{voltage:.3f} В")
            time.sleep(0,5)

    except KeyboardInterrupt:
        print("\n Программа остановлена пользователем")
    finally:
        adc.definit()