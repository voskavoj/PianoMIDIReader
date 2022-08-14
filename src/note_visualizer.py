import time


class NoteVisualizer:
    def __init__(self):
        undef_keys_bottom = ["n/a" for i in range(0, 21)]
        undef_keys_top    = ["n/a" for i in range(109, 128)]
        zero_octave_keys  = ["a0", "a#0", "b0"]
        top_octave_c      = ["c8"]
        standard_keys     = [(note + str(pitch)) for pitch in range(1, 8)
                             for note in ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]]

        self.note_x_midi_map = undef_keys_bottom + zero_octave_keys + standard_keys + top_octave_c + undef_keys_top
        self.notes = {k: 0 for k in self.note_x_midi_map + ["sustain"]}

        self._init_image()

    def loop(self):
        self._show()

    def set_notes(self, notes):
        for note, velocity in notes:
            if note == "p":
                self.notes["pedal"] = 1 if velocity > 0 else 0
            else:
                self.notes[note] = velocity

    def _init_image(self):
        for k in self.notes.keys():
            print(k, end="\t")
        print()

    def _show(self):
        print()
        for k in self.notes.keys():
            print(self.notes[k], end="\t")

# # Create figure for plotting
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# xs = []  # store trials here (n)
# ys = []  # store relative frequency here
# rs = []  # for theoretical probability
#
#
# # This function is called periodically from FuncAnimation
# def animate(i, xs, ys):
#     # Aquire and parse data from serial port
#     line = ser.readline()  # ascii
#     line_as_list = line.split(b',')
#     i = int(line_as_list[0])
#     relProb = line_as_list[1]
#     relProb_as_list = relProb.split(b'\n')
#     relProb_float = float(relProb_as_list[0])
#
#     # Add x and y to lists
#     xs.append(i)
#     ys.append(relProb_float)
#     rs.append(0.5)
#
#     # Limit x and y lists to 20 items
#     # xs = xs[-20:]
#     # ys = ys[-20:]
#
#     # Draw x and y lists
#     ax.clear()
#     ax.plot(xs, ys, label="Experimental Probability")
#     ax.plot(xs, rs, label="Theoretical Probability")
#
#     # Format plot
#     plt.xticks(rotation=45, ha='right')
#     plt.subplots_adjust(bottom=0.30)
#     plt.title('This is how I roll...')
#     plt.ylabel('Relative frequency')
#     plt.legend()
#     plt.axis([1, None, 0, 1.1])  # Use for arbitrary number of trials
#     # plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo
#
#
# # Set up plot to call animate() function periodically
# ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
# plt.show()
