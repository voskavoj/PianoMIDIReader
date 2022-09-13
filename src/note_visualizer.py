import random
import time
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class NoteVisualizer(Thread):
    def __init__(self, ui_style, key_range=("a0", "c8")):
        Thread.__init__(self)
        self._alive = True
        self._index = 0

        # keys
        undef_keys_bottom = ["n/a" for i in range(0, 21)]
        undef_keys_top    = ["n/a" for i in range(109, 128)]
        zero_octave_keys  = ["a0", "a#0", "b0"]
        top_octave_c      = ["c8"]
        standard_keys     = [(note + str(pitch)) for pitch in range(1, 8)
                             for note in ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]]

        # notes
        self.note_x_midi_map = undef_keys_bottom + zero_octave_keys + standard_keys + top_octave_c + undef_keys_top
        i_low, i_high = self.note_x_midi_map.index(key_range[0]), self.note_x_midi_map.index(key_range[1])
        self.note_x_midi_map[:i_low] = ["n/a"] * i_low
        self.note_x_midi_map[i_high+1:] = ["n/a"] * (127 - i_high)
        self.notes = {k: 0 for k in self.note_x_midi_map + ["sustain"]}

        # style
        if ui_style == "console":
            self._show = self._show_console
            self._init_image = self._init_console
        elif ui_style == "gui":
            self._show = self._show_gui
            self._init_image = self._init_gui
        else:
            raise KeyError("Wrong UI style")

    def run(self):
        self._init_image()
        while self._alive:
            self._show()
            time.sleep(0.01)

    def close(self):
        self._alive = False

    def set_notes(self, notes):
        for note, velocity in notes:
            if note == "p":
                self.notes["sustain"] = 1 if velocity > 0 else 0
            else:
                self.notes[self.note_x_midi_map[note]] = velocity

    # overrides _init
    def _init_console(self):
        for k in self.notes.keys():
            if k == "n/a":
                continue
            print(k.rjust(3, ' '), end=" ")
        print()

    # overrides _show
    def _show_console(self):
        print("\r", end="")
        # print()
        for k, n in self.notes.items():
            if k == "n/a":
                continue
            print(str(n).rjust(3, ' '), end=" ")

    # overrides _init
    def _init_gui(self):
        self.size = 50
        fig = plt.figure()
        self.ax = fig.add_subplot(1, 1, 1)
        self.xs = range(self.size)
        self.ys = np.array([[0]*self.size for k in self.notes.keys()])
        ani = animation.FuncAnimation(fig, self._gui_animate, fargs=None, interval=10)
        plt.subplots_adjust(bottom=0.30)
        plt.axis([0, self.size, 0, 128])
        plt.show()

    def _gui_animate(self, arg):
        self.ys[:, 1:] = self.ys[:, :-1]
        self.ys[:, 0] = list(self.notes.values())

        # Draw x and y lists
        self.ax.clear()
        for i in range(len(self.ys)):
            if np.sum(self.ys[i]):  # filter out zero values
                self.ax.plot(self.xs, self.ys[i])
        plt.axis([0, self.size, 0, 128])

    def _show_gui(self):
        print("Never should happen")


if __name__ == "__main__":
    vis = NoteVisualizer("gui")
    vis.start()
    for i in range(1000):
        lst = random.sample([22, 56, 77, 8, 60, 3], 2)
        notes = [(lst[i], random.randint(0, 128)) for i in range(len(lst))]
        vis.set_notes(notes)
        time.sleep(0.2)
        notes = [(lst[i], 0) for i in range(len(lst))]
        vis.set_notes(notes)
        time.sleep(0.1)
    vis.close()
