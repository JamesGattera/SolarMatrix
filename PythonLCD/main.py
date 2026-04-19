from machine import Pin, ADC, PWM, SPI  # type: ignore # CPython IDE
from utime import sleep                 # type: ignore # CPython IDE
import uasyncio as asyncio              # type: ignore # CPython IDE
import display
#import ST7735                          # Indy Lib - Fallback and Reference.

"""
Project Intention:::
Low-power charge controller for two palm-sized solar panels (testing with just one)
Screen displays fun stuff indicating conditions(weather? charge percent?)
Intended:
    External:
        Battery
        Activation trigger on battery (voltage threshold)
Possible:
    OTA - Circuvent security concerns.
    Servo/Motor Tracking/Angling:
        (remember rotation limits for cables)
GPIO Map::
Left Pins(  3.3V  , GND   ,  GPIO15,  GPIO2 , GPIO4 ,  
            GPIO16, GPIO17,  GPIO5 ,  GPIO18, GPIO19, 
            GPIO21, GPIO3 ,  GPIO1 ,  GPIO22, GPIO23,)
Right Pins( VIN   , GND   ,  GPIO13,  GPIO12, GPIO14, 
            GPIO27, GPIO26,  GPIO25,  GPIO33, GPIO32, 
            GPIO35, GPIO34,  GPIO39,  GPIO36, RESET ,)
Hardwired LCD Pins::
PIN_DC   =  2
PIN_RST  =  4
PIN_CS   = 15
PIN_CLK  = 18
PIN_MOSI = 23
PIN_BL   = 32
# Screen size constants :: ACCURATE :: TESTED
LCD_WIDTH  = 320#Tested accurate::panel width
LCD_HEIGHT = 170#Tested accurate::panel height
X_OFFSET = 0  #no side lines hidden. ::is correct
Y_OFFSET = 35 #begins exactly 35 lines down.
Timing Presets (seconds standard)
SpeedTiming = 0.01
CleanTiming = 0.15
EyeTiming   = 0.19
HardTiming  = 0.20
SlowTiming  = 0.75
Panels::
0340 LATE NIGHT : V_Line: 0.674 : V_Load: 0.674 : Amps:I: 0.0030636364 : I:Drop: 0.0 
Cloudy Morning  : 1.8v          : 377       uA  : UNCHECKED %          :
Sunny Midday    : 2.262v        : 2_314_000     : 76935332  %          :
Estimated maximum output: ~3x measured (up to ~6V)
ADC pin reads microvolts (max observed: 3,139,000 µV)
"""

#=====================
# LED pins
Blue_Board_Pin       = Pin( 2, Pin.OUT);Blue_Board_Pin.off()      #DONT USE: TIED DATA/COMMAND BIT.
Green_Breadboard_Pin = Pin(12, Pin.OUT);Green_Breadboard_Pin.off()#Better Visual. More Setup.

#ADC setup
Adc_A = ADC(13) # analog input pin
Adc_B = ADC(14) # analog input pin BRANCH RESISROR
max_uv = 3_139_000  # observed max microvolts
maxUint = 65535
async def avg_uv(adc, samples=5):
    total = 0
    for _ in range(samples):
        total += adc.read_uv()
        sleep(0.001)
    return total // samples


#====================
# MAIN FUNCTION
#=====================
Iter = 0
async def Main():
    "Main Function"
    print('[PROGRAM START]')


    #====================
    # DISPLAY STARTER
    #=====================
    await display.init()
    #await display.fill_screen(display.colour565(0,0,255)) # blue
    #await display.draw_pixel(10,10,display.colour565(255,255,0)) # yellow
    #await display.test_fullscreen()



    #====================
    #ADC AMP READS / PRINTS [WORKING]
    #=====================
    """
    while Iter<10:                                  #TODO: TAILOR
        Iter+=1
        "ADC Loop"

        #Reads
        v_line_uv = avg_uv(Adc_A) #panel direct
        v_load_uv = avg_uv(Adc_B) #panel - bridged resistor
        #Constants
        v_line = v_line_uv / 1_000_000
        v_load = v_load_uv / 1_000_000
        res_val = 220 # Resistor value in ohms #RED RED BLACK BLACK BROWN
        #Maths
        amps      =   v_load / res_val
        amps_drop = ( v_line - v_load ) / res_val
        #Battery Charge Control/ Histeresis                #TODO: TAILOR
        if v_line < 0.01:
            stability = 0
        else:
            stability = v_load / v_line
            if stability > 0.9:
                #transistor_pin.on()  #Power Charging Transistor
                print("Stable")                                           #TODO: BUY MOSFETS
            elif stability > 0.7:
                #transistor_pin.off() #Un-Power Charging Transistor
                print("Unstable")
            else:
                #sleep for physical trigger ???
                print("Off")
        
        #=============
        if Iter % 1 == 0: #Divisible by 10        #TODO: TAILOR
            print(f"{Iter}\tV_Line:{v_line:.3f}\tV_Load:{v_load:.3f}\tI:{amps:.4f}\tDrop:{amps_drop:.6f}\tStab:{stability:.2f}")#TODO: TAILOR
        sleep(1)        #>50 is appropriate      #TODO: TAILOR
        """
    

    #====================
    #HARD ENDING TO MAIN // [WORKING]
    #=====================
    print('[PROGRAM END]')
    #break #clear ending

asyncio.run(Main())
#=====================