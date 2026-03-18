"main.py"


import machine
from utime import sleep


#Side-Show Components ;;
"8-Ohm, 2-Watt speaker"
"Onboard LED"
LED = machine.Pin("LED", machine.Pin.OUT)
Speaker = machine.Pin(27,machine.Pin.OUT)
Freq = 0.005 #Bassy. Working. Preffered Freq. Dont judge.

#Shift Register Pins ;;
"SN74HC595N Shift Register" 
#
# Shift Forward
Shift_srclk = machine.Pin(18, machine.Pin.OUT)#shift in.
# Show Bits
Shift_Rclk = machine.Pin(19, machine.Pin.OUT)
# Input bit 1/0
Shift_input = machine.Pin(20, machine.Pin.OUT)
#
"Shift_OE" #Rail-Grounded.   # Output Enable pin

"5161BS 7/8 segment display"
# 7-segment digits as strings ('0' = HIGH, '1' = LOW)
#One annode linked to High-Rail.
sequence = [1,2,3,4,5,6,7,8,9,0,'DP','A','B','C','D','E','F','G','DP',]

segments = {
    'A': '11111110',
    'B': '11111101',
    'C': '11111011',
    'D': '11110111',
    'E': '11101111',
    'F': '11011111',
    'G': '10111111',
    'DP': '01111111',

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
}



#Functions Block

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
        #
        Shift_srclk.value(1)
        sleep(0.01) # firm delay
        Shift_srclk.value(0)
        sleep(0.01) # firm delay
    Shift_Rclk.value(1)
    sleep(0.01) # firm delay
    Shift_Rclk.value(0)

# Test loop: cycle all segments
if __name__ == '__main__':
    # Flash LED once
    sig() #Init signal.
    
    while True:
        sleep(0.1)
        for key in sequence:
            shift_byte_str(segments[key])
            sleep(0.01) #proof timing. fast loop. splash.
        shift_byte_str('01111111')# Dot Ready.
        #break #testing handbreak.
