import pwm_dac as pwm
import signal_generator as sg
import time

amplitude = 3.2           
signal_frequency = 10     
sampling_frequency = 1000 

try:
    dac = pwm.PWM_DAC(12, 500, 3.3, False)
    
    start_time = time.time()
    
    print("Generating sine wave... Press Ctrl+C to stop")
    print(f"Amplitude: {amplitude} V, Frequency: {signal_frequency} Hz, Sampling: {sampling_frequency} Hz")
    
    while True:
        current_time = time.time() - start_time
        
        normalized_amplitude = sg.get_sin_wave_amplitude(signal_frequency, current_time)
        
        voltage = normalized_amplitude * amplitude
        
        dac.set_voltage(voltage)
        
        sg.wait_for_sampling_period(sampling_frequency)
        
except KeyboardInterrupt:
    print("\nSignal generation stopped by user")
    
finally:
    dac.deinit()
    print("PWM DAC deinitialized")