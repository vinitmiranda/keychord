import mido
import time

# C major scale: C4 D4 E4 F4 G4 A4 B4 C5 (MIDI notes 60-72)
scale_notes = [60, 62, 64, 65, 67, 69, 71, 72]

# List available MIDI output ports
print("Available MIDI output ports:")
for name in mido.get_output_names():
    print(name)

# Open the default output port (or specify one)
outport = mido.open_output("CH345:CH345 MIDI 1 24:0")

for note in scale_notes:
    msg_on = mido.Message('note_on', note=note, velocity=100)
    outport.send(msg_on)
    print(f"Note ON: {note}")
    time.sleep(0.4)  # Hold note for 0.4 seconds
    msg_off = mido.Message('note_off', note=note, velocity=0)
    outport.send(msg_off)
    print(f"Note OFF: {note}")
    time.sleep(0.05)  # Short gap between notes

print("Done playing C major scale.")