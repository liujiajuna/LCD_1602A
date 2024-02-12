import utime
from LCD_1602A import *

lcd = LCD_1602A(RS=0, E=1, D0=2, D1=3, D2=4, D3=5, D4=6, D5=7, D6=8, D7=9)
lcd.init()

columns = 16
lines = 0

Message_Line1 = "    pattern     "
Message_Line2 = range(0, 16)

while 1:
    #generate data
    if lines == 0:
        Message_Line1 = "    pattern     "
        Message_Line2 = range(0, 16)
    else:
        temp = Message_Line1
        Message_Line1 = Message_Line2
        if 255<(lines*columns + 16):
            Message_Line2 = range(lines*columns, 256)
            lines = -1
        else:
            Message_Line2 = range(lines*columns, lines*columns + 16)
        del temp
    #output
    lcd.set_DDRAM_addr(DDRAM_1_LINE_START)
    for data in Message_Line1:
        lcd.write_data(data)

    lcd.set_DDRAM_addr(DDRAM_2_LINE_START)
    for data in Message_Line2:
        lcd.write_data(data)

    lines+=1
    utime.sleep(0.5)

