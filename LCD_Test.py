import utime
from LCD_1602A import *

lcd = LCD_1602A(RS=0, E=1, D0=2, D1=3, D2=4, D3=5, D4=6, D5=7, D6=8, D7=9)
#lcd.init()
lcd.clear()
lcd.function(FUNC_8_BIT|FUNC_2_LINE|FUNC_5_8)
lcd.display(DIS_ON|DIS_CUR_OFF|DIS_CUR_NOT_BLINK)
lcd.entermode(ENTER_INC|ENTER_NOT_SHIFT)

lcd.string("Hello World!")
lcd.set_DDRAM_addr(DDRAM_2_LINE_START)
lcd.string(" 123456789")


direction = 1
step = 4

while True:
    for move in range(0,step):
        if direction == 1:
            lcd.shift(SHIFT_DIS|SHIFT_RIGHT)
        else:
            lcd.shift(SHIFT_DIS|SHIFT_LEFT)
        utime.sleep(0.2)
    else:
        direction = ~direction