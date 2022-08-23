import time

from src.comm import Comm
from src.serial_comm import SerialComm
from src.note_visualizer import NoteVisualizer


class CommunicationHandler:
    def __init__(self, comm: Comm, ui_style, key_range):
        self.vis = NoteVisualizer(ui_style, key_range)
        self.comm = comm
        self.byte_handler = ByteHandler()

        self.comm.open()
        self.vis.start()

        try:
            self._run_midi_communication()
        except KeyboardInterrupt:
            print("Interrupted, closing down")
            self._close()
        except BaseException as exception:
            self._close()
            raise exception

    def _run_midi_communication(self):
        while True:
            if self.comm.is_available():
                time.sleep(0.1)
                notes = self.byte_handler.handle_bytes(self.comm.read())

                self.vis.set_notes(notes)

    def _close(self):
        self.comm.close()
        self.vis.close()


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
    comm = SerialComm(None)
    port = 8  # input("Select serial port: ")
    comm.setup(port, 256000)

    CommunicationHandler(comm, "console", ("c2", "c7"))
