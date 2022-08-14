import time
import serial
import serial.tools.list_ports

from src.note_visualizer import NoteVisualizer


class SerialHandler:
    def __init__(self, port, baud):
        self.vis = NoteVisualizer()
        self.ser = serial.Serial()
        self.byte_handler = ByteHandler()

        self._open_port(port, baud)
        self._loop_midi_communication()
        self.ser.close()

    def _open_port(self, port, baud):
        self.ser.port = f"COM{port}"
        self.ser.baudrate = baud
        self.ser.timeout = 1
        for i in range(1, 11):
            try:
                self.ser.open()
            except serial.SerialException:
                pass

            if self.ser.is_open:
                print("Serial port now open:")
                print(self.ser, "\n")  # print serial parameters
                break
            else:
                print(f"Failed to open serial port at COM{port}. Attempt: {i}/10.")
                time.sleep(1)
        else:
            raise ConnectionError("Failed to open port")

    def _loop_midi_communication(self):
        try:
            while True:
                if self.ser.in_waiting > 0:
                    time.sleep(0.1)
                    notes = self.byte_handler.handle_bytes(self.ser.read(self.ser.in_waiting))

                    self.vis.set_notes(notes)

                # debug
                    self.vis.loop()
        except IOError as e:
            print(e)


class ByteHandler:
    recognised_commands = [0x90, 0xB0, 0xFF]

    def __init__(self):
        self.byte_cnt_even = True  # even = want note; odd = want velocity
        self.pedal = False
        self.invalid_command = True
        self.buffer = []
        self.output = []

    def handle_bytes(self, data: bytes):
        for b in data:
            if b & 0x80 == 0x80:
                self._handle_command_byte(b)
            else:
                self._handle_data_byte(b)
        return self._unload_buffer()

    def _handle_command_byte(self, byte):
        if not self.byte_cnt_even:  # received command when velocity was expected <==> error --> drop last byte
            self.buffer.pop(-1)
            self.byte_cnt_even = True

        self.invalid_command = False
        self.pedal = False

        if byte & 0xF0 == 0xB0:  # sustain pedal
            self.pedal = True
        elif byte not in ByteHandler.recognised_commands:
            self.invalid_command = True
            print(f"WARNING: Unknown command byte: {byte.hex()}")

    def _handle_data_byte(self, byte):
        if self.invalid_command:  # skip all data bytes after non-recognised command
            return

        if self.pedal and self.byte_cnt_even:
            self.buffer.append("p")
        else:
            self.buffer.append(int(byte))

        self.byte_cnt_even = not self.byte_cnt_even

    def _unload_buffer(self):
        buffer_length = len(self.buffer)
        if not buffer_length:  # empty buffer, do nothing
            return

        buffer_copy = self.buffer.copy()
        if buffer_length % 2 == 1:  # odd number of bytes <==> something went wrong --> trim
            buffer_copy.pop(-1)
            self.buffer = self.buffer.pop(-1)
            buffer_length -= 1
        else:
            self.buffer = []

        output = []
        for i in range(0, buffer_length, 2):
            output.append((buffer_copy[i], buffer_copy[i + 1]))

        return output


if __name__ == "__main__":
    ports = serial.tools.list_ports.comports()

    print("COM ports:")
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

    port = input("Select serial port: ")

    SerialHandler(port, 256000)
