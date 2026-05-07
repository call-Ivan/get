import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits  # [22, 27, 17, 26, 25, 21, 20, 16] from MSB to LSB
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)
    
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    
    def set_number(self, number):
        """Set binary number to R2R DAC"""
        for i, pin in enumerate(self.gpio_bits):
            bit = (number >> (7 - i)) & 1  # MSB first
            GPIO.output(pin, bit)
        
        if self.verbose:
            print(f"Number set: {number} (0x{number:02X})")
    
    def set_voltage(self, voltage):
        """Set voltage to R2R DAC"""
        if voltage < 0:
            voltage = 0
        elif voltage > self.dynamic_range:
            voltage = self.dynamic_range
        
        # Convert voltage to number (0-255 for 8-bit DAC)
        number = int((voltage / self.dynamic_range) * 255)
        self.set_number(number)
        
        if self.verbose:
            print(f"Voltage set: {voltage:.3f} V -> number: {number}")

if __name__ == "__main__":
    try:
        dac = R2R_DAC([22, 27, 17, 26, 25, 21, 20, 16], 3.183, True)
        
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
                
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
                
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        
    finally:
        dac.deinit()