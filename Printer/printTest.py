# On the Raspberry Pi with built-in UART:
import serial
import adafruit_thermal_printer
import time 

uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)


ThermalPrinter = adafruit_thermal_printer.get_printer_class(1.0) #2.69


printer = ThermalPrinter(uart)

#if printer.has_paper():
#    print('Printer has paper!')
#else:
#    print('Printer might be out of paper, or RX is disconnected!')
#    


print('Starting Program')    
printer.test_page()

print('Waiting 5 seconds') 
time.sleep(5)

print('Feeding 2 lines ') 
printer.feed(2)

time.sleep(1)

print('Printingsomeshit') 
printer.print('Hello from CircuitPython!')
printer.feed(2)

print('Printing Bold Text') 
printer.bold = True   # Turn on bold
printer.print('This is bold text!')
printer.bold = False  # Turn off bold
# Feed lines to make visible:
printer.feed(2)




#underline - This controls underline printing and can be None (off), adafruit_thermal_printer.UNDERLINE_THIN, or adafruit_thermal_printer.UNDERLINE_THICK.
#size - This controls the size of text and can be adafruit_thermal_printer.SIZE_SMALL, adafruit_thermal_printer.SIZE_MEDIUM, or adafruit_thermal_printer.SIZE_LARGE.  The default is small.
#justify - This controls the justification or location of printed text and can be adafruit_thermal_printer.JUSTIFY_LEFT, adafruit_thermal_printer.JUSTIFY_CENTER, or adafruit_thermal_printer.JUSTIFY_RIGHT.  The default is justify left.