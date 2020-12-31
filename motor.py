import serial
import time

serial_port1 = "COM4"
serial_port2 = "COM5"

def send_serial():
    pass


if __name__ == "__main__":
    motor1 = serial.Serial(
        port = serial_port1,
        baudrate = 57600,
        parity = serial.PARITY_NONE
    )

    motor2 = serial.Serial(
        port = serial_port2,
        baudrate = 57600,
        parity = serial.PARITY_NONE
    )

    # motor1.open()
    # motor2.open()

    # speed mode setup
    motor1.write(bytearray.fromhex("02 00 C4 C6"))
    response = motor1.read(2)
    print(response)
    
    motor1.write(bytearray.fromhex("0A 14 14 32"))
    # response = motor1.read(2)
    # print(response)

    motor2.write(bytearray.fromhex("02 00 C4 C6"))
    # response = motor1.read(2)
    # print(response)
    
    motor2.write(bytearray.fromhex("0A 14 14 32"))
    # response = motor1.read(2)
    # print(response)

    motor1.write(bytearray.fromhex("06 00 88 8E"))
    motor2.write(bytearray.fromhex("06 00 88 8E"))
    # 06 00 88 8E

    # start motor
    motor1.write(bytearray.fromhex("00 00 01 01"))
    motor2.write(bytearray.fromhex("00 00 01 01"))

    time.sleep(5)

    # stop motor
    motor1.write(bytearray.fromhex("00 00 00 00"))
    motor2.write(bytearray.fromhex("00 00 00 00"))
    pass