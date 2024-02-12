import machine
import utime

ENABLE_DELAY                = 0.005

CLEAR                       = 0b00000001
HOME                        = 0b00000010

ENTER                       = 0b00000100
ENTER_INC                   = 0b00000010
ENTER_DEC                   = 0b00000000
ENTER_SHIFT                 = 0b00000001
ENTER_NOT_SHIFT             = 0b00000000

DISPLAY                     = 0b00001000
DISPLAY_ON                  = 0b00000100
DISPLAY_OFF                 = 0b00000000
DISPLAY_CURSOR_ON           = 0b00000010
DISPLAY_CURSOR_OFF          = 0b00000000
DISPLAY_CURSOR_BLINK        = 0b00000001
DISPLAY_CURSOR_NOT_BLINK    = 0b00000000

SHIFT                       = 0b00010000
SHIFT_DISPLAY               = 0b00001000
SHIFT_CURSOR                = 0b00000000
SHIFT_RIGHT                 = 0b00000100
SHIFT_LEFT                  = 0b00000000

FUNCTION                    = 0b00100000
FUNC_8_BIT                  = 0b00010000
FUNC_4_BIT                  = 0b00000000
FUNC_2_LINE                 = 0b00001000
FUNC_1_LINE                 = 0b00000000
FUNC_5X10                   = 0b00000100
FUNC_5X8                    = 0b00000000

CGRAM                       = 0b01000000
DDRAM                       = 0b10000000

DDRAM_1_LINE_START          = 0x00
DDRAM_1_LINE_END            = 0x27
DDRAM_2_LINE_START          = 0x40
DDRAM_2_LINE_END            = 0x67

class LCD_1602A:
    """
    Class for driving a 1602A LCD in MicroPython.
    """

    def __init__(self, RS, E, D0, D1, D2, D3, D4, D5, D6, D7):
        """
        Initialize the LCD_1602A instance.

        :param RS: Register Select pin
        :param E: Enable pin
        :param D0-D7: Data pins
        """
        self.RS = machine.Pin(RS,machine.Pin.OUT)
        self.E  = machine.Pin(E,machine.Pin.OUT)
        self.DATA_PIN = []
        for Data_Pin in (D0, D1, D2, D3, D4, D5, D6, D7):
            self.DATA_PIN.append(machine.Pin(Data_Pin,machine.Pin.OUT))

    def _DATA_PIN_SET(self,data):
        """Set data pins"""
        for index in (0,1,2,3,4,5,6,7):
            if (data>>index) & 0b00000001:
                self.DATA_PIN[index].on()
            else:
                self.DATA_PIN[index].off()

    def _send_command(self, command):
        """
        Send command to LCD by setting RS low.

        :param command: [D7~D0]=[bit7~bit0]
        """
        self.RS.off()
        self._DATA_PIN_SET(command)
        self.E.on()
        utime.sleep(ENABLE_DELAY)
        self.E.off()

    def _send_data(self, data):
        """
        Send data to LCD by setting RS high.

        :param data: [D7~D0]=[bit7~bit0]
        """
        self.RS.on()
        self._DATA_PIN_SET(data)
        self.E.on()
        utime.sleep(ENABLE_DELAY)
        self.E.off()

    def init(self):
        """Initialize the LCD with default settings."""
        self.clear()
        self.function(FUNC_8_BIT|FUNC_2_LINE|FUNC_5X8)
        self.display(DISPLAY_ON|DISPLAY_CURSOR_ON|DISPLAY_CURSOR_BLINK)
        self.entermode(ENTER_INC|ENTER_NOT_SHIFT)

    def clear(self):
        """Clear all display data"""
        self._send_command(CLEAR)

    def home(self):
        """Return cursor to home"""
        self._send_command(HOME)

    def entermode(self,command):
        """
        Set moving direction of cursor and display.

        :param command: ENTER_INC/ENTER_DEC | ENTER_SHIFT/ENTER_NOT_SHIFT
        """
        self._send_command(ENTER | command)

    def display(self,command):
        """
        Set display of LCD,cursor,cursor blinking

        :param command: DISPLAY_ON/DISPLAY_OFF | DISPLAY_CURSOR_ON/DISPLAY_CURSOR_OFF | DISPLAY_CURSOR_BLINK/DISPLAY_CURSOR_NOT_BLINK
        """
        self._send_command(DISPLAY | command)

    def shift(self,command):
        """
        Shift display or cursor

        :param command: SHIFT_DISPLAY/SHIFT_CURSOR | SHIFT_RIGHT/SHIFT_LEFT
        """
        self._send_command(SHIFT | command)

    def function(self,command):
        """
        Set interface data length,number of display lines,character font

        :param command: FUNC_8_BIT/FUNC_4_BIT | FUNC_2_LINE/FUNC_1_LINE | FUNC_5X10/FUNC_5X8
        """
        self._send_command(FUNCTION | command)

    def set_CGRAM_addr(self,address):
        """
        Set CGRAM address

        :param address:6bit Address(bit5~bit0)
        """
        address = address&0x3F
        self._send_command(CGRAM | address)

    def set_DDRAM_addr(self,address):
        """
        Set DDRAM address

        :param address:7bit Address(bit6~bit0)(DDRAM_1_LINE_START/DDRAM_1_LINE_END/DDRAM_2_LINE_START/DDRAM_2_LINE_END)
        """
        address = address&0x7F
        self._send_command(DDRAM | address)

    def read_flag(self,address):
        """
        Read busy flag and set address for read data from LCD(not implemented yet)

        :param address:7bit Address(bit6~bit0)
        """
        pass

    def write_data(self,data):
        """
        Write data to LCD

        :param data:1 integer or character
        """
        if isinstance(data,int):
            self._send_data(data)
        elif isinstance(data,str):
            self._send_data(ord(data))
        else:
            pass

    def read_data(self):
        """
        Read data from LCD(not implemented yet)
        """
        pass

    def string(self,out_str):
        """
        Write string to LCD

        :param out_str:a string output to LCD
        """
        if isinstance(out_str,str):
            for data in out_str:
                self._send_data(ord(data))
        else:
            pass


def main():
    print("#You need new a LCD, Like this:")
    print("LCD = LCD_1602A.LCD_1602A(RS=0, E=1, D0=2, D1=3, D2=4, D3=5, D4=6, D5=7, D6=8, D7=9)")
    print("LCD.init()")
    print("LCD.string(\"Hello World\")")

if __name__ == '__main__':
    main()
