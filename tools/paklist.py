"""List the files of a UE4 pak (v3/v4, unencrypted index). paklist.py <pak> [substring ...]"""
import struct, sys
def entries(path):
    f = open(path, "rb"); f.seek(0, 2); n = f.tell()
    f.seek(n - 45); tail = f.read(45)
    enc = tail[0]; magic, ver, off, size = struct.unpack_from("<IIQQ", tail, 1)
    assert magic == 0x5A6F12E1, hex(magic)
    if enc: raise SystemExit("encrypted index")
    f.seek(off); ix = f.read(size); p = 0
    def fstr():
        nonlocal p
        l = struct.unpack_from("<i", ix, p)[0]; p += 4
        if l < 0: s = ix[p:p - 2 * l].decode("utf-16le"); p += -2 * l
        else: s = ix[p:p + l].decode("latin1"); p += l
        return s.rstrip("\0")
    mount = fstr(); cnt = struct.unpack_from("<i", ix, p)[0]; p += 4
    for _ in range(cnt):
        name = fstr()
        o, sz, usz, comp = struct.unpack_from("<QQQI", ix, p); p += 28 + 20
        if comp: nb = struct.unpack_from("<I", ix, p)[0]; p += 4 + 16 * nb
        p += 1 + 4  # encrypted flag, block size
        yield mount + name, o, sz, usz, comp
if __name__ == "__main__":
    keys = [k.lower() for k in sys.argv[2:]]
    for name, o, sz, usz, comp in entries(sys.argv[1]):
        if not keys or any(k in name.lower() for k in keys):
            print(name, usz)
