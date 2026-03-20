// main.c

///// Includes /////
//Necessary::
#include <stdio.h>
//ESP-IDF::
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

/*
Okay, New Project,
Our intention here is to::
1) get the LCD working 
    1.0) via Bit-Banging 
    1.1) while enjoying Stretch-Goals
SDA  -> GPIO23  (MOSI)
SCL  -> GPIO18  (SCLK)
CS   -> GPIO15
RS   -> GPIO2   (DC)
RST  -> GPIO4
VDO  -> 3.3V
LEDA -> 3.3V
LEDK -> GPIO32
GND  -> GND
*/

// Configs //
//LCD Pins::
#define PIN_MOSI 23
#define PIN_SCLK 18
#define PIN_CS   15
#define PIN_DC   2
#define PIN_RST  4
#define PIN_BL   32 //Works to control on-off (output.)

//TimingPresets (MS in whole integer.)::
#define SpeedTiming  10     // Test Speed (Dodge WDT) over 9 under 10
#define CleanTiming  15    // Comfortable, Between *Watchdog and *Flicker
#define EyeTiming    19   // Slowest Invisible Cycle. Under 20. (I stared until: no-flicker point)
#define HardTiming   20  // Enough for a clear latch
#define SlowTiming  750 // Enough for 'calm' visual// "Waiting Cursor"

///// Main /////
void app_main(void)
{
    vTaskDelay(pdMS_TO_TICKS(500)); //Clears Boot-Loop Confusion Before Behaviour.
    gpio_set_direction(PIN_BL, GPIO_MODE_OUTPUT); //Backlight Pin - Output.
    gpio_set_level(PIN_BL, 0); //Backlight Off Before Program.

    while (true) {
        gpio_set_level(PIN_BL, 1);  //Backlight On
        vTaskDelay(pdMS_TO_TICKS(CleanTiming));

        gpio_set_level(PIN_BL, 0);//Backlight Off
        vTaskDelay(pdMS_TO_TICKS(CleanTiming));
    }
}
