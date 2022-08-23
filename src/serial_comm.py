import time
import serial
import serial.tools.list_ports

from src.comm import Comm


class SerialComm(Comm):
    def __init__(self, port, baud=256000, timeout=1):
        Comm.__init__(self)
        self.ser = serial.Serial()

        if port is None:
            ports = serial.tools.list_ports.comports()
            print("COM ports:")
            for port, desc, hwid in sorted(ports):
                print("{}: {} [{}]".format(port, desc, hwid))
        else:
            self.setup(port, baud, timeout)

    def setup(self, port, baud=256000, timeout=1):
        self.ser.port = f"COM{port}"
        self.ser.baudrate = baud
        self.ser.timeout = timeout

    def open(self, max_attempts=10):
        for i in range(1, max_attempts + 1):
            try:
                self.ser.open()
            except serial.SerialException:
                pass

            if self.ser.is_open:
                print("Serial port now open:")
                print(self.ser, "\n")  # print serial parameters
                break
            else:
                print(f"Failed to open serial port at {self.ser.port}. Attempt: {i}/10.")
                time.sleep(1)
        else:
            raise ConnectionError("Failed to open port")

    def close(self):
        self.ser.close()

    def is_available(self):
        return self.ser.in_waiting > 0

    def number_available(self):
        return self.ser.in_waiting

    def read(self, number=None):
        if number is None:
            number = self.ser.in_waiting
        return self.ser.read(number)
