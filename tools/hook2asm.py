#!/usr/bin/env python3
"""
Turn a Gemini transcription answer into pokered music asm.

    python3 tools/hook2asm.py answer.txt --label Music_CrystalMotif

Reads the exact block docs/music-prompts.md asks Gemini for:

    KEY:    D minor
    TEMPO:  92
    METER:  4/4
    HOOK:   D4/1 F4/1 A4/2 G4/1 F4/1 D4/2
    BASS:   D3/4 Bb2/2 A2/2
    CHORDS: Dm | Dm | Bb | A
    FEEL:   ...
    DOUBT:  ...

and emits three channels, checked. It refuses rather than guesses: a hook that
does not parse, or channels that do not total the same length, stops the run.
Nobody downstream can hear the difference, so the arithmetic is the only
error-detection there is.

Durations are in beats; --ticks sets how many engine units a beat is worth
(4 by default, so a beat is a quarter note against note_type 12).
"""
import sys, re, argparse

NOTES = {'C':'C_','C#':'C#','DB':'C#','D':'D_','D#':'D#','EB':'D#','E':'E_',
         'FB':'E_','F':'F_','F#':'F#','GB':'F#','G':'G_','G#':'G#','AB':'G#',
         'A':'A_','A#':'A#','BB':'A#','B':'B_','CB':'B_'}
# 7.2: octave-folded visible spectrum, red = C.
SPECTRUM = {'C':'red','C#':'red-orange','D':'orange','D#':'yellow','E':'yellow-green',
            'F':'green','F#':'green-blue','G':'blue','G#':'indigo','A':'violet',
            'A#':'(no wavelength)','B':'(no wavelength)'}

def parse_seq(s):
    """'D4/1 F4/1 A4/2' -> [('D_', 4, 1.0), ...]"""
    out = []
    for tok in s.split():
        m = re.fullmatch(r'([A-Ga-g][#b]?)(-?\d)/(\d+(?:\.\d+)?)', tok.strip())
        if not m:
            raise ValueError("cannot parse note %r -- expected e.g. D4/1" % tok)
        name = m.group(1).upper().replace('B', 'B') if len(m.group(1)) == 1 else m.group(1).upper()
        key = NOTES.get(name) or NOTES.get(m.group(1).upper())
        if not key: raise ValueError("unknown pitch %r" % m.group(1))
        out.append((key, int(m.group(2)), float(m.group(3))))
    return out

def emit(seq, ticks, indent='\t'):
    lines, cur_oct, total = [], None, 0
    for pitch, octv, beats in seq:
        n = int(round(beats * ticks))
        if n < 1 or n > 16:
            raise ValueError("note length %d out of range 1..16 (beats=%s, --ticks=%d)" % (n, beats, ticks))
        if octv != cur_oct:
            lines.append("%soctave %d" % (indent, octv)); cur_oct = octv
        lines.append("%snote %s, %d" % (indent, pitch, n)); total += n
    return lines, total

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('answer'); ap.add_argument('--label', default='Music_Motif')
    ap.add_argument('--ticks', type=int, default=4)
    a = ap.parse_args()
    txt = open(a.answer).read()
    def field(name):
        m = re.search(r'^\s*%s:\s*(.+)$' % name, txt, re.M | re.I)
        return m.group(1).strip() if m else None

    if 'NO AUDIO' in txt.upper():
        sys.exit("answer says NO AUDIO -- the file did not reach Gemini. Nothing to convert.")

    key, tempo, hook, bass = field('KEY'), field('TEMPO'), field('HOOK'), field('BASS')
    if not hook: sys.exit("no HOOK field found")
    for label, val in (('KEY', key), ('TEMPO', tempo)):
        if not val or val.lower().startswith('unsure'):
            print("  !! %s is %s -- fill it before this is used in a town theme" % (label, val or 'missing'))

    if key:
        root = re.match(r'([A-Ga-g][#b]?)', key)
        if root:
            r = root.group(1).upper()
            hue = SPECTRUM.get(NOTES.get(r, '').replace('_', ''), None) or SPECTRUM.get(r)
            print("  KEY %-10s -> 7.2 reads that pitch as %s" % (key, hue or 'unmapped'))

    print("  TEMPO %s\n" % (tempo or '?'))
    hs, ht = emit(parse_seq(hook), a.ticks)
    print("%s_Ch1::" % a.label)
    if tempo and tempo.isdigit(): print("\ttempo %s" % tempo)
    print("\tvolume 7, 7\n\tduty_cycle 2\n\tnote_type 12, 11, 3\n.mainloop:")
    print('\n'.join(hs)); print("\tsound_loop 0, .mainloop\n\n\tsound_ret\n")

    if bass and not bass.lower().startswith('unsure'):
        bs, bt = emit(parse_seq(bass), a.ticks)
        print("%s_Ch3::" % a.label)
        print("\tnote_type 12, 1, 2\n.mainloop:")
        print('\n'.join(bs)); print("\tsound_loop 0, .mainloop\n\n\tsound_ret\n")
        if bt != ht:
            print("  !! HOOK is %d units and BASS is %d -- they will drift apart." % (ht, bt))
            print("     Pad the shorter one before using this.")
        else:
            print("  channels agree at %d units." % ht)
    else:
        print("  (no BASS given -- hook is %d units)" % ht)

if __name__ == '__main__':
    main()
