"main.py"
import machine #includes ADC, Pin
from utime import sleep #Lighter Sleep Functions.

#Side-Show Components ;;
"8-Ohm, 2-Watt speaker" #too heavy for present setup
"Onboard LED"
"SN74HC595N Shift Register"
LED = machine.Pin("LED", machine.Pin.OUT)
Speaker = machine.Pin(27,machine.Pin.OUT)
Freq = 0.005 #Bassy. Working. Preffered Freq. Dont judge.
Shift_srclk = machine.Pin(2, machine.Pin.OUT) #shift in.
Shift_Rclk = machine.Pin(1, machine.Pin.OUT) #Show Bits.
Shift_input = machine.Pin(0, machine.Pin.OUT) #Input bit 1/0.
"Shift_OE" #Rail-Grounded. # Output Enable pin
"5161BS 7/8 segment display"
#10 pins, Common(middle) annode linked to High-Rail.
# 8-segment pins from strings ('0' = HIGH, '1' = LOW)

#==Output Presets==
#All Possible::
SequenceA = [1,2,3,4,5,6,7,8,9,0,
             'A','B','C','D','E','F','G','DP',]
#4 Circle::
SequenceB = ['G', 'C', 'D', 'E',]
#6 Circle::
SequenceC = ['A', 'B', 'C', 'D', 'E', 'F',]
#dot blink
SequenceD = ['DP', 'CLR']

segments = {
    #Segments spiral inward clockwise-clockface.
    #A is uppermost, G is middle, DP is dot.
    'A':    '11111110',
    'B':    '11111101',
    'C':    '11111011',
    'D':    '11110111',
    'E':    '11101111',
    'F':    '11011111',
    'G':    '10111111',
    'DP':   '01111111',
    'CLR':  '11111111',

    #Numeric Patterns
    0: '11000000',
    1: '11111001',
    2: '10100100',
    3: '10110000',
    4: '10011001',
    5: '10010010',
    6: '10000010',
    7: '11111000',
    8: '10000000',
    9: '10010000',

    #Improvised Letters/Symbols
    'a':    '10001000', #capital
    'b':    '10000011', #lowercase
    'c':    '11000110', #capital
    'd':    '10100001', #lowercase
    'e':    '10000110', #uppercase
    'f':    '10001110', #uppercase
    'h':    '10001001', #uppercase
    'j':    '11110001', #barely works
    'l':    '11000111', #uppercase, getting tired of writing these lol.
    'HY':  '10111111', #a hyphen/dash, middle light
}
SequenceX = ['CLR', 'HY',] #the one im working mapping characters
#==Functions Block==

# Init Block
"Sound and Flash for 0.25 seconds"
def sig(): #for Signal.
    LED.value(1)
    shift_byte_str('01111111')#Working Dot.
    for _ in range(25): #Quarter-second Output.
        pass # Ive disconnected the speaker for now - lower physical complexity
        Speaker.value(1)
        sleep(Freq) #on
        Speaker.value(0)
        sleep(Freq) #off
    LED.value(0)

# Byte Pusher
def shift_byte_str(byte_str):
    Shift_Rclk.value(0)  #ensures latch-LOW
    for bit in byte_str: #flip: reversed(byte_str):
        Shift_input.value(int(bit))
        
        Shift_srclk.value(1)
        sleep(FastTiming) # fast delay
        Shift_srclk.value(0)
        sleep(FastTiming) # fast delay
    
    Shift_Rclk.value(1)
    sleep(HardTiming) # firm delay
    Shift_Rclk.value(0)

#==Presets Block==
FastTiming = 0.0005# lowest 'solid' speed is 0.0009 #0.001 is visible cycle.
HardTiming = 0.001 # enough for a clear latch
SlowTiming = 0.75 # enough for 'calm' visual

if __name__ == '__main__':
    sig() #Init signal.
    while True:
        Sequence = SequenceX
        for key in Sequence:
            shift_byte_str(segments[key])
            sleep(SlowTiming)    
        #break
