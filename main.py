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
#Rail-Powered and Rail-Gounded
#Output-Enable Rail-Low (Bright/Decisive)
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
#Both annodes linked to High-Rail.
digits = {
    0: '00111111',
    1: '00000110',
    2: '01011011',
    3: '01001111',
    4: '01100110',
    5: '01101101',
    6: '01111101',
    7: '00000111',
    8: '01111111',
    9: '01101111'
}

segments = {
    'A': '00000001',
    'B': '00000010',
    'C': '00000100',
    'D': '00001000',
    'E': '00010000',
    'F': '00100000',
    'G': '01000000',
    'DP':'10000000'
}



#Functions Block

# Init Block
"Sound and Flash for 0.25 seconds"
def sig(): #for Signal.
    LED.value(1)
    for _ in range(25): #Quarter-second flash.
        pass # Ive disconnected the speaker for now - lower physical complexity
        Speaker.value(1)
        sleep(Freq) #on
        Speaker.value(0)
        sleep(Freq) #off
    LED.value(0)

# Byte Pusher
def shift_byte_str(byte_str):
    Shift_Rclk.value(0)  #ensures latch-LOW
    for bit in reversed(byte_str):
        Shift_input.value(int(bit))
        #
        Shift_srclk.value(1)
        sleep(0.01) # firm delay
        Shift_srclk.value(0)
        sleep(0.01) # firm delay
    Shift_Rclk.value(1)
    sleep(0.01) # firm delay
    Shift_Rclk.value(0)

"""Display a single digit on 7-segment."""
def display_number(n):
    # Display number 0-9
    if 0 <= n <= 9:
        shift_byte_str(digits[n])

# Test loop: cycle all segments
if __name__ == '__main__':
    # Flash LED once
    LED.value(1)
    sleep(0.25)
    LED.value(0)
    
    while True:
        shift_byte_str('11111111')
        sleep(1)

        shift_byte_str('00000000')
        sleep(1)