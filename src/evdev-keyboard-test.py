import evdev
import mido
from typing import Final

CODE_CHORD_MAP = {
    evdev.ecodes.KEY_TAB: [60, 64, 67],
    evdev.ecodes.KEY_Q: [61, 65, 68],
    evdev.ecodes.KEY_W: [62, 66, 69],
    evdev.ecodes.KEY_E: [63, 67, 70],
    evdev.ecodes.KEY_R: [64, 68, 71],
    evdev.ecodes.KEY_T: [65, 69, 72],
    evdev.ecodes.KEY_Y: [66, 70, 73],
    evdev.ecodes.KEY_U: [67, 71, 74],
    evdev.ecodes.KEY_I: [68, 72, 75],
    evdev.ecodes.KEY_O: [69, 73, 76],
    evdev.ecodes.KEY_P: [70, 74, 77],
    evdev.ecodes.KEY_LEFTBRACE: [59, 63, 66],
    evdev.ecodes.KEY_RIGHTBRACE: [60, 64, 67],
    evdev.ecodes.KEY_CAPSLOCK: [60, 63, 67],
    evdev.ecodes.KEY_A: [61, 64, 68],
    evdev.ecodes.KEY_S: [62, 65, 69],
    evdev.ecodes.KEY_D: [63, 66, 70],
    evdev.ecodes.KEY_F: [64, 67, 71],
    evdev.ecodes.KEY_G: [65, 68, 72],
    evdev.ecodes.KEY_H: [66, 69, 73],
    evdev.ecodes.KEY_J: [67, 70, 74],
    evdev.ecodes.KEY_K: [68, 71, 75],
    evdev.ecodes.KEY_L: [69, 72, 76],
    evdev.ecodes.KEY_SEMICOLON: [60, 64, 67],
    evdev.ecodes.KEY_APOSTROPHE: [61, 65, 68],
    evdev.ecodes.KEY_LEFTSHIFT: [60, 64, 67, 70],
    evdev.ecodes.KEY_Z: [61, 65, 68, 71],
    evdev.ecodes.KEY_X: [62, 66, 69, 72],
    evdev.ecodes.KEY_C: [63, 67, 70, 73],
    evdev.ecodes.KEY_V: [64, 68, 71, 74],
    evdev.ecodes.KEY_B: [65, 69, 72, 75],
    evdev.ecodes.KEY_N: [66, 70, 73, 76],
    evdev.ecodes.KEY_M: [67, 71, 74, 77],
    evdev.ecodes.KEY_COMMA: [68, 72, 75, 78],
    evdev.ecodes.KEY_DOT: [69, 73, 76, 79],
    evdev.ecodes.KEY_SLASH: [70, 74, 77, 80],
    evdev.ecodes.KEY_RIGHTSHIFT: [71, 75, 78, 81],
}
CC_REVERB: Final[int] = 91
CC_CHORUS: Final[int] = 93
MAX_VELOCITY: Final[int] = 127
CHANNEL: Final[int] = 0
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
keyboard = evdev.InputDevice("/dev/input/event7")
outport = mido.open_output("CH345:CH345 MIDI 1 24:0")


def get_device_capabilities(device):
    capabilities = device.capabilities(verbose=True)
    for event_type, event_name_code_tuple_list in capabilities.items():
        if event_type[1] == evdev.ecodes.EV_KEY:
            for event_name, event_code in event_name_code_tuple_list:
                print(f"{event_name} {event_code}")


def map_code_to_midi(code, code_midi_map):
    if code in code_midi_map:
        midi_notes = code_midi_map[code]
    return (CHANNEL, midi_notes)


def set_code_note_map(code):
    global code_note_map
    if code in CODE_CHORD_MAP.keys() and len(CODE_CHORD_MAP[code]) == 3:
        code_note_map = {
            evdev.ecodes.KEY_1: CODE_CHORD_MAP[code][0],
            evdev.ecodes.KEY_2: CODE_CHORD_MAP[code][1],
            evdev.ecodes.KEY_3: CODE_CHORD_MAP[code][2],
            evdev.ecodes.KEY_4: CODE_CHORD_MAP[code][0] + 12,
            evdev.ecodes.KEY_5: CODE_CHORD_MAP[code][1] + 12,
            evdev.ecodes.KEY_6: CODE_CHORD_MAP[code][2] + 12,
            evdev.ecodes.KEY_7: CODE_CHORD_MAP[code][0] + 24,
            evdev.ecodes.KEY_8: CODE_CHORD_MAP[code][1] + 24,
            evdev.ecodes.KEY_9: CODE_CHORD_MAP[code][2] + 24,
            evdev.ecodes.KEY_0: CODE_CHORD_MAP[code][0] + 36,
        }
    elif code in CODE_CHORD_MAP.keys() and len(CODE_CHORD_MAP[code]) == 4:
        code_note_map = {
            evdev.ecodes.KEY_1: CODE_CHORD_MAP[code][0],
            evdev.ecodes.KEY_2: CODE_CHORD_MAP[code][1],
            evdev.ecodes.KEY_3: CODE_CHORD_MAP[code][2],
            evdev.ecodes.KEY_4: CODE_CHORD_MAP[code][3],
            evdev.ecodes.KEY_5: CODE_CHORD_MAP[code][0] + 12,
            evdev.ecodes.KEY_6: CODE_CHORD_MAP[code][1] + 12,
            evdev.ecodes.KEY_7: CODE_CHORD_MAP[code][2] + 12,
            evdev.ecodes.KEY_8: CODE_CHORD_MAP[code][3] + 12,
            evdev.ecodes.KEY_9: CODE_CHORD_MAP[code][0] + 24,
            evdev.ecodes.KEY_0: CODE_CHORD_MAP[code][1] + 24,
            evdev.ecodes.KEY_MINUS: CODE_CHORD_MAP[code][2] + 24,
            evdev.ecodes.KEY_EQUAL: CODE_CHORD_MAP[code][3] + 24,
        }


def send_midi_note_on(channel, midi_notes, velocity):
    for midi_note in midi_notes:
        msg = mido.Message(
            "note_on", note=midi_note, velocity=velocity, channel=channel
        )
        outport.send(msg)


def send_midi_note_off(channel, midi_notes):
    for midi_note in midi_notes:
        msg = mido.Message("note_off", note=midi_note, channel=channel)
        outport.send(msg)


def send_midi_cc(channel, cc_number, cc_value):
    msg = mido.Message(
        "control_change", channel=channel, control=cc_number, value=cc_value
    )
    outport.send(msg)


def device_listen(device):
    print(f"Listening on {device.name} ({device.path})...")
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY and event.code in CODE_CHORD_MAP:
            set_code_note_map(event.code)
            channel, notes = map_code_to_midi(event.code, CODE_CHORD_MAP)
            if event.value == 1:
                send_midi_note_on(channel, notes, VELOCITY)
            else:
                send_midi_note_off(channel, notes)
        elif event.type == evdev.ecodes.EV_KEY and event.code in code_note_map:
            channel, notes = map_code_to_midi(event.code, code_note_map)
            if event.value == 1:
                send_midi_note_on(channel, notes, VELOCITY)
            else:
                send_midi_note_off(channel, notes)
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


get_device_capabilities(keyboard)
