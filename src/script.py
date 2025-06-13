import evdev
import mido
from typing import Final

CODE_CHORD_MAP = {
    evdev.ecodes.KEY_TAB: [61, 65, 68],    # Db major
    evdev.ecodes.KEY_Q: [68, 72, 75],      # Ab major
    evdev.ecodes.KEY_W: [63, 67, 70],      # Eb major
    evdev.ecodes.KEY_E: [70, 74, 77],      # Bb major
    evdev.ecodes.KEY_R: [65, 69, 72],      # F major
    evdev.ecodes.KEY_T: [60, 64, 67],      # C major
    evdev.ecodes.KEY_Y: [67, 71, 74],      # G major
    evdev.ecodes.KEY_U: [62, 66, 69],      # D major
    evdev.ecodes.KEY_I: [69, 73, 76],      # A major
    evdev.ecodes.KEY_O: [64, 68, 71],      # E major
    evdev.ecodes.KEY_P: [71, 75, 78],      # B major
    evdev.ecodes.KEY_LEFTBRACE: [66, 70, 73], # Gb major
    evdev.ecodes.KEY_CAPSLOCK: [61, 64, 68],  # Db minor
    evdev.ecodes.KEY_A: [68, 71, 75],      # Ab minor
    evdev.ecodes.KEY_S: [63, 66, 70],      # Eb minor
    evdev.ecodes.KEY_D: [70, 73, 77],      # Bb minor
    evdev.ecodes.KEY_F: [65, 69, 72],      # F minor
    evdev.ecodes.KEY_G: [60, 63, 67],      # C minor
    evdev.ecodes.KEY_H: [67, 70, 74],      # G minor
    evdev.ecodes.KEY_J: [62, 65, 69],      # D minor
    evdev.ecodes.KEY_K: [69, 72, 76],      # A minor
    evdev.ecodes.KEY_L: [64, 67, 71],      # E minor
    evdev.ecodes.KEY_SEMICOLON: [71, 74, 78], # B minor
    evdev.ecodes.KEY_APOSTROPHE: [66, 69, 73], # Gb minor
    evdev.ecodes.KEY_LEFTSHIFT: [61, 65, 68, 71], # Db 7 
    evdev.ecodes.KEY_Z: [68, 72, 75, 78],  # Ab 7
    evdev.ecodes.KEY_X: [63, 67, 70, 73],  # Eb 7
    evdev.ecodes.KEY_C: [70, 74, 77, 80],  # Bb 7
    evdev.ecodes.KEY_V: [65, 69, 72, 75],  # F 7
    evdev.ecodes.KEY_B: [60, 64, 67, 70],  # C 7
    evdev.ecodes.KEY_N: [67, 71, 74, 77],  # G 7
    evdev.ecodes.KEY_M: [62, 66, 69, 72],  # D 7
    evdev.ecodes.KEY_COMMA: [69, 73, 76, 79], # A 7
    evdev.ecodes.KEY_DOT: [64, 68, 71, 74], # E 7
    evdev.ecodes.KEY_SLASH: [71, 75, 78, 81], # B 7
    evdev.ecodes.KEY_RIGHTSHIFT: [66, 70, 73, 76], # Gb 7
}

CC_REVERB: Final[int] = 91
CC_CHORUS: Final[int] = 93
MAX_VELOCITY: Final[int] = 127
NOTE_CHANNEL: Final[int] = 0
CHORD_CHANNEL: Final[int] = 1
VELOCITY: Final[int] = 127

code_note_map = {
    evdev.ecodes.KEY_1: [48],
    evdev.ecodes.KEY_2: [52],
    evdev.ecodes.KEY_3: [55],
    evdev.ecodes.KEY_4: [60],
    evdev.ecodes.KEY_5: [64],
    evdev.ecodes.KEY_6: [67],
    evdev.ecodes.KEY_7: [72],
    evdev.ecodes.KEY_8: [76],
    evdev.ecodes.KEY_9: [79],
    evdev.ecodes.KEY_0: [84],
}
cc_memory = {
    CC_REVERB: 0,
    CC_CHORUS: 0,
}
outport = mido.open_output("BlueALSA:BLE MIDI Server 128:0")
last_code = None

def find_keyboard_device():
    for dev_path in evdev.list_devices():
        device = evdev.InputDevice(dev_path)
        capabilities = device.capabilities()
        if evdev.ecodes.EV_KEY in capabilities:
            return device
    raise RuntimeError("No keyboard device found.")

keyboard = find_keyboard_device()


def get_device_capabilities(device):
    capabilities = device.capabilities(verbose=True)
    for event_type, event_name_code_tuple_list in capabilities.items():
        if event_type[1] == evdev.ecodes.EV_KEY:
            for event_name, event_code in event_name_code_tuple_list:
                print(f"{event_name} {event_code}")


def map_code_to_midi(code, code_midi_map):
    if code in code_midi_map:
        midi_notes = code_midi_map[code]
    return midi_notes


def set_code_note_map(code):
    global code_note_map
    if code in CODE_CHORD_MAP.keys() and len(CODE_CHORD_MAP[code]) == 3:
        code_note_map = {
            evdev.ecodes.KEY_1: [CODE_CHORD_MAP[code][0]],
            evdev.ecodes.KEY_2: [CODE_CHORD_MAP[code][1]],
            evdev.ecodes.KEY_3: [CODE_CHORD_MAP[code][2]],
            evdev.ecodes.KEY_4: [CODE_CHORD_MAP[code][0] + 12],
            evdev.ecodes.KEY_5: [CODE_CHORD_MAP[code][1] + 12],
            evdev.ecodes.KEY_6: [CODE_CHORD_MAP[code][2] + 12],
            evdev.ecodes.KEY_7: [CODE_CHORD_MAP[code][0] + 24],
            evdev.ecodes.KEY_8: [CODE_CHORD_MAP[code][1] + 24],
            evdev.ecodes.KEY_9: [CODE_CHORD_MAP[code][2] + 24],
            evdev.ecodes.KEY_0: [CODE_CHORD_MAP[code][0] + 36],
        }
    elif code in CODE_CHORD_MAP.keys() and len(CODE_CHORD_MAP[code]) == 4:
        code_note_map = {
            evdev.ecodes.KEY_1: [CODE_CHORD_MAP[code][0]],
            evdev.ecodes.KEY_2: [CODE_CHORD_MAP[code][1]],
            evdev.ecodes.KEY_3: [CODE_CHORD_MAP[code][2]],
            evdev.ecodes.KEY_4: [CODE_CHORD_MAP[code][3]],
            evdev.ecodes.KEY_5: [CODE_CHORD_MAP[code][0] + 12],
            evdev.ecodes.KEY_6: [CODE_CHORD_MAP[code][1] + 12],
            evdev.ecodes.KEY_7: [CODE_CHORD_MAP[code][2] + 12],
            evdev.ecodes.KEY_8: [CODE_CHORD_MAP[code][3] + 12],
            evdev.ecodes.KEY_9: [CODE_CHORD_MAP[code][0] + 24],
            evdev.ecodes.KEY_0: [CODE_CHORD_MAP[code][1] + 24],
            evdev.ecodes.KEY_MINUS: [CODE_CHORD_MAP[code][2] + 24],
            evdev.ecodes.KEY_EQUAL: [CODE_CHORD_MAP[code][3] + 24],
        }


def send_midi_notes_on(channel, midi_notes, velocity):
    for midi_note in midi_notes:
        msg = mido.Message(
            "note_on", note=midi_note, velocity=velocity, channel=channel
        )
        outport.send(msg)
        print(f"Note ON: {midi_note} (Channel: {channel}, Velocity: {velocity})")


def send_midi_notes_off(channel, midi_notes):
    for midi_note in midi_notes:
        msg = mido.Message("note_off", note=midi_note, channel=channel)
        outport.send(msg)
        print(f"Note OFF: {midi_note} (Channel: {channel})")


def send_midi_cc(channel, cc_number, cc_value):
    msg = mido.Message(
        "control_change", channel=channel, control=cc_number, value=cc_value
    )
    outport.send(msg)


def device_listen(device):
    print(f"Listening on {device.name} ({device.path})...")
    global last_code
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY and event.code in CODE_CHORD_MAP:
            if event.value == 1:
                if last_code is not None:
                    prev_notes = map_code_to_midi(last_code, CODE_CHORD_MAP)
                    send_midi_notes_off(CHORD_CHANNEL, prev_notes)
                set_code_note_map(event.code)
                notes = map_code_to_midi(event.code, CODE_CHORD_MAP)
                send_midi_notes_on(CHORD_CHANNEL, notes, VELOCITY)
                last_code = event.code
            
        elif event.type == evdev.ecodes.EV_KEY and event.code in code_note_map:
            notes = map_code_to_midi(event.code, code_note_map)
            if event.value == 1:
                send_midi_notes_on(NOTE_CHANNEL, notes, VELOCITY)
            elif event.value == 0:
                send_midi_notes_off(NOTE_CHANNEL, notes)
        elif event.type == evdev.ecodes.EV_REL:
            global cc_memory
            if event.code == evdev.ecodes.REL_X:
                cc_memory[CC_CHORUS] += event.value
                cc_memory[CC_CHORUS] = max(0, min(MAX_VELOCITY, cc_memory[CC_CHORUS]))
                send_midi_cc(0, CC_CHORUS, cc_memory[CC_CHORUS])
            elif event.code == evdev.ecodes.REL_Y:
                cc_memory[CC_REVERB] += event.value
                cc_memory[CC_REVERB] = max(0, min(MAX_VELOCITY, cc_memory[CC_REVERB]))
                send_midi_cc(0, CC_REVERB, cc_memory[CC_REVERB])


device_listen(keyboard)