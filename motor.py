import serial
import typing

class Motor:
    """[Wrapper class for motor driver serial(RS232) communication]
    """

    NOT_INITIALIZED = 0
    SPEED_MODE = 1
    TORQUE_MODE = 2
    POSITION_MODE = 3

    def __init__(self,port, baudrate=57600, parity=serial.PARITY_NONE):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity
        )
        self.mode = self.SPEED_MODE

    def __hex_converter(self, max, scale):
        # value / max * scale => hex(str)
        return lambda v : hex(int(v / max * scale))

    def __scaler(self, max, scale, len):
        # TODO: rename function
        # value / max * scale % 256 => int
        return lambda v : [(int(v / max * scale) & (0xFF<<(m*8))) >>(m*8) for m in range(len)].reverse()

    def run(self):
        self.ser.write(bytearray.fromhex("00 00 01 01"))
    
    def stop(self):
        self.ser.write(bytearray.fromhex("00 00 00 00"))
        #TODO: check respond
    
    def send_serial(self, *data):
        #TODO: need to check data length?
        #TODO: handle other dataset except int
        msg = ""
        for d in data:
            # assert len(d) > 0 and len(d) <=2
            msg += "{:02X} ".format(d)

        self.ser.write(msg)

    def send_serial_checksum(self, *data, checksum=True):
        #TODO: need to check data length?
        #TODO: handle other dataset except int
        if checksum:
            check = sum(data) % 256
            self.send_serial(*data, check)
        else:
            self.send_serial(*data)
        pass

    def read_serial(self):
        #TODO: implement
        pass

    def init_speed_mode(self, acc_time:float=1, dcc_time:float=1):
        acdc_time = self.__scaler(max=1, scale=1, len=1)
        
        acc = acdc_time(acc_time)
        dcc = acdc_time(dcc_time)

        self.ser.write(bytearray.fromhex("02 00 C4 C6")) # PC speed mode
        # self.ser.write(bytearray.fromhex("0A {0} {1} "))
        self.send_serial_checksum(0x0A, acc, dcc) # acc/dcc
        
        pass

    def set_rpm(self, rpm:int):
        rpm_hex = self.__scaler(max=3000, scale=8192, len=2)
        rpm_converted = rpm_hex(rpm)
        assert len(rpm_hex) == 2
        self.send_serial_checksum(0x06, rpm_converted[0], rpm_converted[1])