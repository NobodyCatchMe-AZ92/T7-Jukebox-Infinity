"""Tekken 7 .usm video encryption - make your own background video playable by the game.

The game's CRI Mana player decrypts every video packet (@SFV chunk, data type 0) of a .usm with two 32-byte masks
(mask1 = ~mask2). A plain Sofdec Prime encode is therefore 'decrypted' into garbage and shows black. This tool
encrypts a plain encode the same way the game's own videos are, so the game shows it.

The masks are not stored here: `recover` derives them from one of YOUR game's own videos (statistically: in the
chained part of every packet the encrypted byte equals plain[i] ^ plain[i-32] ^ mask2[i & 31], and plain[i] ==
plain[i-32] is by far the most common case, so the most common byte per column is mask2), and writes them to a small
file that `encrypt` / `verify` read. Read-only on the game files.

  usm_crypt.py recover <game .usm> <masks out>        e.g. Content/Movies/Ui/MainMenuCS_01.usm (takes ~15 s)
  usm_crypt.py verify  <masks> <game .usm>            decrypt + re-encrypt every packet, compare (proves the masks)
  usm_crypt.py encrypt <masks> <plain .usm> <out>     encrypt a plain Sofdec Prime .usm for the game

Your video: Sofdec Prime (MPEG-1 style, CRI codec 1), 1920x1080, 30 fps, no audio - the game's menu videos are
the same. The Jukebox mod plays it from Win64/t7jukebox/Jukebox Background.usm.
"""
import struct
import sys
from collections import Counter

KEY1 = KEY2 = b""


def load_masks(path):
    global KEY1, KEY2
    KEY2 = bytes.fromhex(open(path, encoding="ascii").read().split()[0])
    if len(KEY2) != 32:
        sys.exit("masks file: expected 64 hex digits")
    KEY1 = bytes(x ^ 0xFF for x in KEY2)


def chunks(d):
    o = 0
    while o + 0x20 <= len(d):
        size = struct.unpack(">I", d[o + 4:o + 8])[0]
        poff = d[o + 9]
        pad = struct.unpack(">H", d[o + 10:o + 12])[0]
        typ = d[o + 15]
        yield o, d[o:o + 4], typ, o + 8 + poff, o + 8 + size - pad
        o += 8 + size


def decrypt(p):
    b = bytearray(p)
    size = len(b) - 0x40
    if size >= 0x200:
        m = bytearray(KEY2)
        for i in range(0x100, size):
            b[0x40 + i] ^= m[i & 31]
            m[i & 31] = b[0x40 + i] ^ KEY2[i & 31]
        m = bytearray(KEY1)
        for i in range(0x100):
            m[i & 31] ^= b[0x100 + 0x40 + i]
            b[0x40 + i] ^= m[i & 31]
    return bytes(b)


def encrypt(p):
    b = bytearray(p)
    size = len(b) - 0x40
    if size >= 0x200:
        plain = bytes(b)
        m = bytearray(KEY1)  # first 0x100 bytes: chained on the PLAIN bytes 0x100..0x1FF
        for i in range(0x100):
            m[i & 31] ^= plain[0x100 + 0x40 + i]
            b[0x40 + i] = plain[0x40 + i] ^ m[i & 31]
        m = bytearray(KEY2)
        for i in range(0x100, size):
            b[0x40 + i] = plain[0x40 + i] ^ m[i & 31]
            m[i & 31] = plain[0x40 + i] ^ KEY2[i & 31]
    return bytes(b)


def is_plain(d):
    for o, sig, typ, a, z in chunks(d):
        if sig == b"@SFV" and typ == 0 and z - a > 0x240:
            return b"\x00\x00\x01\x01" in d[a + 0x40:a + 0x400]
    return False


def recover(d):
    cols = [Counter() for _ in range(32)]
    for o, sig, typ, a, z in chunks(d):
        if sig == b"@SFV" and typ == 0 and z - a - 0x40 >= 0x200:
            p = d[a:z]
            for i in range(0x120, len(p) - 0x40):
                cols[i & 31][p[0x40 + i]] += 1
    if not cols[0]:
        sys.exit("no encrypted video packets found")
    return bytes(c.most_common(1)[0][0] for c in cols)


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    if sys.argv[1] == "recover":
        m = recover(open(sys.argv[2], "rb").read())
        open(sys.argv[3], "w", encoding="ascii").write(m.hex() + chr(10))
        print(f"masks written to {sys.argv[3]} - check them with: usm_crypt.py verify {sys.argv[3]} {sys.argv[2]}")
        return
    load_masks(sys.argv[2])
    del sys.argv[2]
    if sys.argv[1] == "verify":
        d = open(sys.argv[2], "rb").read()
        n = bad = 0
        for o, sig, typ, a, z in chunks(d):
            if sig == b"@SFV" and typ == 0:
                p = d[a:z]
                if encrypt(decrypt(p)) != p:
                    bad += 1
                n += 1
        print(f"{n} packets, {bad} mismatches, plain={is_plain(d)}")
    elif sys.argv[1] == "encrypt":
        d = bytearray(open(sys.argv[2], "rb").read())
        if not is_plain(d):
            sys.exit("input is not a plain Sofdec Prime .usm")
        n = 0
        for o, sig, typ, a, z in list(chunks(bytes(d))):
            if sig == b"@SFV" and typ == 0:
                p = bytes(d[a:z])
                e = encrypt(p)
                assert decrypt(e) == p
                d[a:z] = e
                n += 1
        open(sys.argv[3], "wb").write(d)
        print(f"encrypted {n} packets -> {sys.argv[3]}, plain now={is_plain(bytes(d))}")


if __name__ == "__main__":
    main()
