"""Parse a plain Wwise bank (Tekken 7 AkBankBGM.bnk) and report sources: object type, id, plugin, stream type,
source id, in-memory size, and the file offset of the stream-type byte. Read-only."""
import struct
import sys
from collections import Counter

p = open(sys.argv[1], "rb").read()
chunks = {}
o = 0
while o < len(p):
    tag, sz = p[o:o + 4].decode(), struct.unpack_from("<I", p, o + 4)[0]
    chunks[tag] = (o + 8, sz)
    o += 8 + sz
print({k: (hex(v[0]), v[1]) for k, v in chunks.items()})
ver = struct.unpack_from("<I", p, chunks["BKHD"][0])[0]
print("bank version", ver)
didx = {}
if "DIDX" in chunks:
    s, n = chunks["DIDX"]
    for i in range(0, n, 12):
        mid, off, size = struct.unpack_from("<III", p, s + i)
        didx[mid] = (off, size)
print("DIDX entries", len(didx))
s, n = chunks["HIRC"]
cnt = struct.unpack_from("<I", p, s)[0]
o = s + 4
types = Counter()
rows = []
for _ in range(cnt):
    t = p[o]
    sz = struct.unpack_from("<I", p, o + 1)[0]
    body = o + 5
    types[t] += 1
    oid = struct.unpack_from("<I", p, body)[0]
    if t == 2:  # Sound: id, AkBankSourceData{plugin u32, stream u8, sourceID u32, inMemSize u32, bits u8}
        plugin, st, sid, msz = struct.unpack_from("<IBII", p, body + 4)
        rows.append(("sound", oid, plugin, st, sid, msz, body + 8))
    elif t == 11:  # Music Track: id, flags u8, numSources u32, then sources
        flags = p[body + 4]
        ns = struct.unpack_from("<I", p, body + 5)[0]
        q = body + 9
        for k in range(ns):
            plugin, st, sid, msz = struct.unpack_from("<IBII", p, q)
            rows.append(("mtrack", oid, plugin, st, sid, msz, q + 4))
            q += 14
    o = body + sz
print("HIRC types", dict(types))
st = Counter((r[0], r[3]) for r in rows)
print("sources by (obj, streamtype)", dict(st))
want = set(int(x) for x in sys.argv[2:])
for r in rows:
    if not want or r[4] in want:
        print(f"{r[0]:6s} obj {r[1]:>10} plugin {r[2]:#x} stream {r[3]} source {r[4]:>10} memsize {r[5]:>7} "
              f"stream_byte_off {r[6]:#x} didx {didx.get(r[4])}")
