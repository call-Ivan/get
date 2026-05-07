import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        """
        Конструктор класса R2R_ADC.
        
        Аргументы:
            dynamic_range (float): динамический диапазон (опорное напряжение) в вольтах.
            compare_time (float, optional): время ожидания после установки кода ЦАП
                                             для стабилизации компаратора (секунды).
                                             По умолчанию 0.01 с.
            verbose (bool, optional): если True, печатать отладочную информацию.
                                      По умолчанию False.
        """
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        # Номера GPIO-пинов 8-битного R-2R ЦАП (от старшего бита к младшему)
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        # Номер GPIO-пина, подключённого к выходу компаратора
        self.comp_gpio = 21

        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        # Пины ЦАП настраиваем как выходы с начальным состоянием 0
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        # Пин компаратора настраиваем как вход
        GPIO.setup(self.comp_gpio, GPIO.IN)

        if self.verbose:
            print(f"R2R_ADC инициализирован: dynamic_range={self.dynamic_range} В, "
                  f"compare_time={self.compare_time} с")

    def deinit(self):
        """Деструктор: выставляем 0 на выход ЦАП и очищаем настройки GPIO."""
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()
        if self.verbose:
            print("R2R_ADC деинициализирован")

    def number_to_dac(self, number):
        """
        Подаёт число (0–255) на вход ЦАП.
        
        Аргументы:
            number (int): число от 0 до 255.
        """
        # Ограничиваем число допустимыми пределами
        number = max(0, min(255, number))
        
        # Подаём биты: первый пин в списке — старший бит (MSB)
        for i, pin in enumerate(self.bits_gpio):
            # bit7 (вес 128) -> i=0, bit6 -> i=1, ... , bit0 -> i=7
            bit = (number >> (7 - i)) & 1
            GPIO.output(pin, bit)
        
        if self.verbose:
            print(f"number_to_dac: подано число {number}")

    def sequential_counting_adc(self):
        """
        Последовательно (перебором) подаёт числа на ЦАП до тех пор,
        пока напряжение ЦАП не превысит входное напряжение АЦП.
        
        Возвращает:
            int: последнее поданное число (код), при котором компаратор сработал.
                 Если напряжение на входе АЦП превышает максимальное возможное
                 напряжение ЦАП, возвращает 255.
        """
        # Перебираем коды от 0 до 255
        for code in range(256):
            # Подаём текущий код на ЦАП
            self.number_to_dac(code)
            
            # Делаем паузу для стабилизации компаратора (по умолчанию 0.01 с)
            time.sleep(self.compare_time)
            
            # Читаем выход компаратора:
            # Если на пине comp_gpio 1, значит напряжение ЦАП >= напряжение АЦП
            if GPIO.input(self.comp_gpio):
                if self.verbose:
                    print(f"sequential_counting_adc: компаратор сработал на коде {code}")
                return code
        
        # Если ни разу не сработали (входное напряжение выше диапазона ЦАП)
        if self.verbose:
            print("sequential_counting_adc: входное напряжение выше диапазона, возвращаем 255")
        return 255

    def get_sc_voltage(self):
        """
        Измеряет напряжение на входе АЦП методом последовательного счёта.
        
        Возвращает:
            float: напряжение в вольтах.
        """
        code = self.sequential_counting_adc()
        voltage = (code / 255.0) * self.dynamic_range
        
        if self.verbose:
            print(f"get_sc_voltage: код {code} -> напряжение {voltage:.3f} В")
        
        return voltage


# ============================================================
# Основной охранник (entry point)
# ============================================================
if __name__ == "__main__":
    # ВНИМАНИЕ: измерьте реальное опорное напряжение мультиметром!
    # Обычно оно около 3.30 В, но может отличаться.
    # Подставьте своё значение.
    DYNAMIC_RANGE = 3.30      # <-- ИЗМЕРЬТЕ И ПОДСТАВЬТЕ ВАШЕ ЗНАЧЕНИЕ

    try:
        # Создаём объект класса R2R_ADC
        adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=0.01, verbose=True)

        print(f"\nНачало измерений (динамический диапазон = {DYNAMIC_RANGE} В)")
        print("Нажмите Ctrl+C для остановки\n")

        # Бесконечный цикл измерений
        while True:
            voltage = adc.get_sc_voltage()
            print(f"{voltage:.3f} В")
            time.sleep(0.5)   # пауза между измерениями для удобства

    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")
    finally:
        # Обязательно вызываем деструктор
        adc.deinit()