# display.py

from machine import Pin, SPI    # type: ignore # CPython IDE
from utime import sleep         # type: ignore # CPython IDE
import uasyncio as asyncio      # type: ignore # CPython IDE

"""
ST7735 SPI LCD Driver for ESP32-WROOM-32 Integral_LCD

- Top-left origin, pixels increment right/down
- Handles RGB/BGR panel inversion (255-0)
- Simple functions for commands, data, pixel, and screen fill
- Comments for debug

Pins are hardwired:
    PIN_MOSI = 23  # SPI data out
    PIN_CLK  = 18  # SPI clock
    PIN_CS   = 15  # Chip Select
    PIN_DC   = 2   # Data/Command
    PIN_RST  = 4   # Reset
    PIN_BL   = 32  # Backlight
"""

# Hardware Pins
PIN_DC   =  2
PIN_RST  =  4
PIN_CS   = 15
PIN_CLK  = 18
PIN_MOSI = 23
PIN_BL   = 32

# SPI object;baudrate tested to 1_000_000_000, wouldnt want to break it lol
spi = SPI(2, baudrate=25_000_000, polarity=0, phase=0)

# Control pin abstractions
cs  = Pin(PIN_CS, Pin.OUT) #Chip Select(Choose This Device)
dc  = Pin(PIN_DC, Pin.OUT) #Data/Command
rst = Pin(PIN_RST, Pin.OUT)#Reset
bl  = Pin(PIN_BL, Pin.OUT) #Backlight

# Screen size constants :: ACCURATE :: TESTED
LCD_WIDTH  = 320#Tested accurate::panel width
LCD_HEIGHT = 170#Tested accurate::panel height
X_OFFSET = 0  #no side lines hidden. ::is correct
Y_OFFSET = 35 #begins exactly 35 lines down.

# Helper functions: core of this module
"Low-Level Writes"
def cmd(c):
    """Send a single command byte to the LCD."""
    dc.value(0)   # command mode
    cs.value(0)
    spi.write(bytearray([c]))
    cs.value(1)
def data(d):
    """Send a single data byte to the LCD."""
    dc.value(1)   # data mode
    cs.value(0)
    spi.write(bytearray([d]))
    cs.value(1)
def data_buf(buf):
    "Buffer                                            "
    dc.value(1)
    cs.value(0)
    spi.write(buf)
    cs.value(1)

# Initialization ( Confirmed Works. )
def init():
    """Reset and init LCD."""
    # Hardware reset
    rst.value(0)
    sleep(0.1)
    rst.value(1)#RST
    sleep(0.1)

    # exit low-power mode
    cmd(0x11)  # Sleep Out(CMD)
    sleep(0.01)

    # Memory Data Access Control (MADCTL)
    # 0x00 = Normal: top-left origin, increment right/down, RGB color order
    cmd(0x36)   #MADCTL::
    data(0xA0)  #0x00 = normal (no flip)            ::top-right down, right to left
                #0x40 = horizontal flip (MX=1)      ::bottom-right up, Right-left
                #0x88 = RGB-to-BGR PLUS ABOVE
                #0x80 = vertical flip (MY=1)        ::top-left down , left - right
                #0xC0 = both flips (MX=1, MY=1)     ::bottom-left up, left-right
                #0x20 = flips XY priority
                #0xA0 = flips XY AND flips vertically

    # Pixel Format
    cmd(0x3A)  # COLMOD
    data(0x05) # 16-bit RGB565

    # Turn on display
    cmd(0x29)  # Display ON
    sleep(0.1)

    # Turn on backlight
    bl.value(0)

# Color helper
def colour565(r, g, b):
    """
    Convert 8-bit RGB to 16-bit RGB565 for inverted panel:
    panel expects 0=full, 255=off per channel
    Swap channels if panel is BGR
    """
    r = 255 - r
    g = 255 - g
    b = 255 - b
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

# Windowing/Pixel Drawing
def set_window(x0, y0, x1, y1):

    col_start = x0 + X_OFFSET
    col_end   = x1 + X_OFFSET

    row_start = y0 + Y_OFFSET
    row_end   = y1 + Y_OFFSET

    cmd(0x2A)
    data(col_start >> 8); data(col_start & 0xFF)
    data(col_end   >> 8); data(col_end   & 0xFF)

    cmd(0x2B)
    data(row_start >> 8); data(row_start & 0xFF)
    data(row_end   >> 8); data(row_end   & 0xFF)

    cmd(0x2C)


def draw_pixel(x, y, colour):
    """
    Draw a single pixel at (x, y) with RGB565 color.
    invert XY for cheapo board
    """
    set_window(x, y, x, y)  # Across=X Down=Y
    dc.value(1)
    cs.value(0)
    # Send high byte first, then low byte
    spi.write(bytearray([colour >> 8, colour & 0xFF]))
    cs.value(1)
#draw_pixel(0,0,colour565(255,0,0))#single pixel working

def fill_screen(color):
    set_window(0, 0, LCD_WIDTH-1, LCD_HEIGHT-1)

    hi = color >> 8
    lo = color & 0xFF
    buf = bytearray([hi, lo] * 64)

    dc.value(1)
    cs.value(0)

    for _ in range((LCD_WIDTH * LCD_HEIGHT) // 64):
        spi.write(buf)

    cs.value(1)
#fill_screen(colour565(255,0,0))

# ---------------------------
# End of driver
# ---------------------------
#
COL = colour565(255,255,255) # colour565(255,255,255)
#
def test_fullscreen():
    init()
    """
    Fill the visible screen with a gradient using proper XY orientation.
    Row-based buffering (correct for MADCTL with MV set).
    """
    for y in range(LCD_HEIGHT):  # vertical (down)
        # Preallocate full row buffer (faster + avoids heap fragmentation)
        row_buf = bytearray(LCD_WIDTH * 2)
        for x in range(LCD_WIDTH):  # horizontal (across)
            r = int((x / (LCD_WIDTH - 1)) * 255)
            g = int((y / (LCD_HEIGHT - 1)) * 255)
            b = 255
            color = colour565(r, g, b)
            idx = x * 2
            row_buf[idx]     = color >> 8
            row_buf[idx + 1] = color & 0xFF
        # IMPORTANT: end coords are inclusive → subtract 1
        set_window(0, y, LCD_WIDTH - 1, y)
        #
        dc.value(1)
        cs.value(0)
        spi.write(row_buf)
        cs.value(1)
#test_fullscreen()
#
def Square_Test():
    init()

    draw_pixel(0, 0, COL)
    draw_pixel(50, 0, COL)
    draw_pixel(0, 50, COL)
    draw_pixel(50, 50, COL)
#Square_Test()
#
def test_batch(batch_rows=1):#170 rows, looking into even divisions: 32 is 1 a second, whole screen is generally slow.
    """
    Fill the screen with a gradient using row batching.
    batch_rows: number of rows per SPI transaction.
    Faster than single-row writes.
    """
    init()  # Ensure MADCTL and offsets are set correctly
    #
    for start_y in range(0, LCD_HEIGHT, batch_rows):
        # Determine actual number of rows in this batch
        rows = min(batch_rows, LCD_HEIGHT - start_y)
        # Preallocate buffer: rows × width × 2 bytes per pixel
        buf = bytearray(rows * LCD_WIDTH * 2)
        #
        for row in range(rows):
            y = start_y + row
            for x in range(LCD_WIDTH):
                r = 255 #int((x / (LCD_WIDTH - 1)) * 255)
                g = 255 #int((y / (LCD_HEIGHT - 1)) * 255)
                b = 0
                color = colour565(r, g, b)
                idx = (row * LCD_WIDTH + x) * 2
                buf[idx]     = color >> 8
                buf[idx + 1] = color & 0xFF
        # Set window for this batch
        set_window(0, start_y, LCD_WIDTH - 1, start_y + rows - 1)
        # Send batch over SPI
        dc.value(1)
        cs.value(0)
        spi.write(buf)
        cs.value(1)
#test_batch()
print("[DISPLAY INITIALIZED]")