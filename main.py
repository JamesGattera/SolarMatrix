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
"SN74HC595N Shift Register" #powered and gounded
# Shift Forward
Shift_srclk = machine.Pin(18, machine.Pin.OUT)#shift in.
# Show Bits
Shift_Rclk = machine.Pin(19, machine.Pin.OUT)
# Input bit 1/0
Shift_input = machine.Pin(20, machine.Pin.OUT)

#7 Segment Display Lookups ;;
"5161BS 7/8 segment display"
digits = {
    0: 0b11000000,  # Segments A B C D E F ON
    1: 0b11111001,  # Segments B C ON
    2: 0b10100100,  # Segments A B D E G ON
    3: 0b10110000,  # Segments A B C D G ON
    4: 0b10011001,  # Segments B C F G ON
    5: 0b10010010,  # Segments A C D F G ON
    6: 0b10000010,  # Segments A C D E F G ON
    7: 0b11111000,  # Segments A B C ON
    8: 0b10000000,  # Segments A B C D E F G ON
    9: 0b10010000   # Segments A B C D F G ON
}
# Optional: segment labels if you want single segment testing
segments = {
    'A': 0b00000001,
    'B': 0b11111101,
    'C': 0b11111011,
    'D': 0b11110111,
    'E': 0b11101111,
    'F': 0b11011111,
    'G': 0b10111111,
    'DP':0b01111111
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
def shift_byte(byte):
    "Send Single Byte to Shift Register"
    for I in range(8):
        """
        # Determine which bit to send (start with MostSignificantBit(MSB))
        bit_position = 7 - i
        shifted_byte = byte >> bit_position  # shift the target bit to LeastSegnificantBit(LSB)
        current_bit = shifted_byte & 0b00000001  # isolate that bit (0 or 1)
        Shift_input.value(current_bit)  # write bit to data pin
        """
        Shift_input.value((byte >> ( 7 - I )) & 1)
        Shift_srclk.value(1)
        Shift_srclk.value(0)
    Shift_Rclk.value(1)
    Shift_Rclk.value(0)

def display_number(n):
    """Display a single digit on 7-segment."""
    if 0 <= n <= 9:
        shift_byte(digits[n])

#Main Loop
"""
1, Indicate working.
2, Read charge percentage.
3, Send signals to Register.
4, Strech goals:
A, Duty cycle for cooling.
B, Incorporate advanced display.
C, scary maths.
"""
if __name__ == '__main__':
    sig() #Indicate Startup
    counter = 0

    while True:
        "The big thing right now;"
        "is getting a relaible printout"
        "We're Lit but inverted via Annode."
        "Try a Push;;"

        for seg, byte in segments.items():
            print(f"Testing segment {seg}")
            shift_byte(byte)          # use byte ^ 0xFF if inverted logic
            sleep(1)