import fluidsynth
import time

scale_notes = [60, 62, 64, 65, 67, 69, 71, 72]

fs = fluidsynth.Synth()
fs.start(driver="alsa")
sfid = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
fs.program_select(0, sfid, 0, 0)

fs.cc(0, 7, 100) 
fs.cc(0, 10, 64)
#set sustain
fs.cc  
for note in scale_notes:
    fs.noteon(0, note, 120)  # channel, midi note, velocity
    print(f"Note ON: {note}")
    time.sleep(0.4)  # Hold note for 0.4 seconds
    print(f"Note OFF: {note}")
    fs.noteoff(0, note)
    time.sleep(0.05)  # Short gap between notes


