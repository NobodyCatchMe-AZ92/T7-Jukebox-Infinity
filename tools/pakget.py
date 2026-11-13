"""Extract files from a UE4 pak (unencrypted). pakget.py <pak> <outdir> <substring> ..."""
import os, struct, sys, zlib
sys.path.insert(0, os.path.dirname(__file__))
from paklist import entries
def read(f, o, sz, usz, comp):
    f.seek(o); hdr = f.read(53)
    _, csz, usz2, c = struct.unpack_from("<QQQI", hdr, 0)
    p = 48
    if c:
        f.seek(o + 48); nb = struct.unpack("<I", f.read(4))[0]
        blocks = [struct.unpack("<QQ", f.read(16)) for _ in range(nb)]
        out = b""
        for a, b in blocks:
            f.seek(a); out += zlib.decompress(f.read(b - a))
        return out
    f.seek(o + 53); return f.read(usz)
if __name__ == "__main__":
    pak, out, keys = sys.argv[1], sys.argv[2], sys.argv[3:]
    f = open(pak, "rb")
    for name, o, sz, usz, comp in entries(pak):
        if any(k in name for k in keys):
            d = read(f, o, sz, usz, comp)
            dst = os.path.join(out, os.path.basename(name)); open(dst, "wb").write(d)
            print(os.path.basename(name), len(d), usz)
