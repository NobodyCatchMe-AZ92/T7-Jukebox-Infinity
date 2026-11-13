"""Minimal GFx/SWF tag dumper (uncompressed 'GFX'/'FWS' inside a uasset). Dev helper.
  gfx_dump.py <uasset> [filter]  -> sprites with frame labels and named placements, external images, exports"""
import struct, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
NAMES = {1001: "DefineExternalImage", 1009: "DefineExternalImage2", 56: "ExportAssets", 76: "SymbolClass", 57: "ImportAssets", 71: "ImportAssets2", 1008: "DefineSubImage"}
def rect_len(d, p):
    n = d[p] >> 3; return (5 + 4 * n + 7) // 8
def tags(d, p, end):
    while p < end:
        h = struct.unpack_from("<H", d, p)[0]; p += 2; code, ln = h >> 6, h & 63
        if ln == 63: ln = struct.unpack_from("<I", d, p)[0]; p += 4
        yield code, d[p:p + ln]; p += ln
        if code == 0: return
def cstr(b, p):
    e = b.index(b"\0", p); return b[p:e].decode("latin1"), e + 1
def place(b, code):
    if code == 26: f = b[0]; p = 1; depth = struct.unpack_from("<H", b, p)[0]; p += 2
    else: f = b[0]; f2 = b[1]; p = 2; depth = struct.unpack_from("<H", b, p)[0]; p += 2
    if code == 70 and (f2 & 8 or (f2 & 16 and f & 2)): _, p = cstr(b, p)
    cid = None
    if f & 2: cid = struct.unpack_from("<H", b, p)[0]; p += 2
    name = None
    if f & 32:
        # skip matrix / cxform: too fiddly; search the name heuristically at the end
        pass
    return depth, cid, f
def main():
    d = open(sys.argv[1], "rb").read(); flt = sys.argv[2] if len(sys.argv) > 2 else None
    o = d.find(b"GFX"); ln = struct.unpack_from("<I", d, o + 4)[0]; s = d[o:o + ln]
    p = 8 + rect_len(s, 8) + 4
    chars = {}
    for code, b in tags(s, p, len(s)):
        if code in (1001, 1009):
            cid = struct.unpack_from("<H", b, 0)[0]; print("ext image", code, "id", cid, b[:60])
        elif code == 56:
            n = struct.unpack_from("<H", b, 0)[0]; q = 2
            for _ in range(n):
                cid = struct.unpack_from("<H", b, q)[0]; nm, q = cstr(b, q + 2); chars[cid] = nm
                if not flt or flt in nm: print("export", cid, nm)
        elif code in (57, 71):
            print("import", b[:200])
        elif code == 39:
            sid = struct.unpack_from("<H", b, 0)[0]; frame = 0; out = []
            for c2, b2 in tags(b, 4, len(b)):
                if c2 == 1: frame += 1
                elif c2 == 43: out.append(f"f{frame}:label={cstr(b2, 0)[0]}")
                elif c2 in (26, 70):
                    try: depth, cid, f = place(b2, c2)
                    except struct.error: depth, cid, f = -1, None, 0
                    nm = None
                    if f & 32:
                        z = b2.rstrip(b"\0").split(b"\0")
                        cand = b2[:-1] if b2.endswith(b"\0") else b2
                    names = [x.decode("latin1") for x in b2.split(b"\0") if x.endswith(b"_mc") or x.startswith(b"Rep_") or x.startswith(b"DT_") or x.startswith(b"Panel")]
                    out.append(f"f{frame}:place d{depth} c{cid} {names[-1][-40:] if names else ''}")
            txt = " | ".join(out)
            if not flt or flt in txt or str(sid) == flt: print("sprite", sid, chars.get(sid, ""), "frames", frame, txt[:3000])
main()
