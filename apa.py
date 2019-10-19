"""APA102 module

Includes the Apa102 class making use of bit-bang to transmit data
"""
from time import sleep_us # pylint: disable=import-error, no-name-in-module
from machine import Pin # pylint: disable=import-error

class Apa102():
    """APA102 driver-class

    Non-SPI/bit-bang & uses a matrix in which the values are written
    to and sendt from.
    Use led_update to transmit the data manually after changing the
    arrays.

    Variables:
        brightness {str} -- Sets the default brightness, 8-bit value,
            first three need to be high
        led_count {number} -- How many LEDs there are
        led_matrix {list} -- List of lists containing each LED's balues
        startframe {list} -- Frame that shows start of transmission
            when sendt
        endframe {list} -- Frame that shows end of transmission
            when sendt
        status_led_count {number} -- [description]
        Single_LED_BRG_values {list} -- Array used to populate the
            matrix whith default values
    """
    brightness = "11100001"  # 225
    led_count = 0
    led_matrix = []
    startframe = ["00000000"]*4
    endframe = ["11111111"]*4
    Single_LED_BRG_values = ["00000000"]*4

    def __init__(self, brightness, clk_pin, data_pin, led_count):
        """__init__

        Arguments:
            brightness {int} -- brightness of LEDs
            clk_pin {int} -- Which pin to use as clock out
            data_pin {int} -- Which pin to use as data out
            led_count {int} -- How many LEDS are connected / to be used
        """
        self.data_pin = Pin(data_pin, Pin.OUT)
        self.clk_pin = Pin(clk_pin, Pin.OUT)
        self.brightness = brightness
        self.Single_LED_BRG_values[0] = '{0:08b}'.format(brightness)
        self.led_count = led_count
        self.led_matrix = [None] * led_count
        #
        for i in range(led_count):
            self.led_matrix[i] = self.Single_LED_BRG_values

    def send_data(self, data):
        """Transmits parsed data to LEDs

        Bit-bangs the clock pin while setting the data pin equal to
            the data supplied.

        Arguments:
            data {list} -- data of single LED
        """
        for array in data:
            for string in array:
                for value in string:
                    self.data_pin.value(int(value))
                    sleep_us(5)
                    self.clk_pin.value(1)
                    sleep_us(10)
                    self.clk_pin.value(0)
                    sleep_us(5)
                    self.data_pin.value(0)
                    sleep_us(5)

    def send_startframe(self):
        """Transmits the startframe

        Transmits 4 arrays of 8 1s being the startframe for the APA102
        """
        self.send_data(self.startframe)

    def send_endframe(self):
        """Transmits the endframe

        Transmits 4 arrays of 8 0s being the endframe for the APA102
        """
        self.send_data(self.endframe)

    def send_colour(self, amount):
        """Transmits the colours of the LEDs

        Transmits the colours of the LEDs from index 0 to amount parsed
            from the led_matrix

        Arguments:
            amount {int} -- The amount of LEDs colours should be sendt
                to
        """
        for i in range(amount):
            self.send_data(self.led_matrix[i])

    def led_update(self):
        """Updates LEDs according to led_matrix

        Sends startframe then data contained in led_matrix and
            then the endframe
        """
        self.send_startframe()
        self.send_colour(self.led_count)
        self.send_endframe()

    def bgr_to_led_values(self, brightness, bgr_values): # pylint: disable=no-self-use
        """Creates a list of LED values from parsed values

        Formats the parsed values into 8-bit strings and returns those

        Arguments:
            brightness {int} -- brightness of LEDs
            bgr_values {list} -- Contains values for Blue,
                Green & Red (BGR)
        """
        return ['{0:08b}'.format(brightness),
                '{0:08b}'.format(bgr_values[0]),
                '{0:08b}'.format(bgr_values[1]),
                '{0:08b}'.format(bgr_values[2])]

    def change_led_colour(self, bgr_values):
        """Changes LED colours to parsed values

         and updates all
            LEDs in the matrix with said values

        Arguments:
            bgr_values {list} -- Contains values for Blue,
                Green & Red (BGR)
        """
        for i in range(self.led_count):
            self.led_matrix[i] = bgr_to_led_values(self.brightness, # pylint: disable=undefined-variable
                                                   bgr_values)
            self.led_update()

    def change_single_led(self, led_index, brightness, bgr_values):
        """Changes a single LED to parsed colours

        Changes the values of the LED according to the parsed index
            (0-n) to the parsed values.
        led_update has to be called manually to update the LEDs
            afterwards

        Arguments:
            led_index {list} -- Which LED's data to update
            brightness {int} -- brightness of LED
            bgr_values {list} -- Contains values for Blue,
                Green & Red (BGR)
        """
        for i in led_index:
            self.led_matrix[i] = bgr_to_led_values(brightness, bgr_values) # pylint: disable=undefined-variable
