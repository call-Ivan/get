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
        self.pwm.start(0)
        
        if self.verbose:
            print(f"PWM DAC initialized on pin {self.gpio_pin} at {self.pwm_frequency} Hz")
    
    def deinit(self):
        """Stop PWM and cleanup GPIO"""
        self.pwm.stop()
        GPIO.cleanup(self.gpio_pin)
        
        if self.verbose:
            print("PWM DAC deinitialized")
    
    def set_voltage(self, voltage):
        if voltage < 0:
            voltage = 0
        elif voltage > self.dynamic_range:
            voltage = self.dynamic_range
        
        duty_cycle = (voltage / self.dynamic_range) * 100
        
        self.pwm.ChangeDutyCycle(duty_cycle)
        
        if self.verbose:
            print(f"Voltage set: {voltage:.3f} V -> duty cycle: {duty_cycle:.1f}%")

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.290, True)
        
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