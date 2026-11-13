"""Scan every WwiseAudio .wem in the game's pakchunk paks (read-only): codec, channels, length, smpl loop points.
Marks the media the BGM / Tekken Bowl banks use and the media the Jukebox browser lists. Dev tool.
  wem_scan.py <paks dir> <AkBankBGM plain dump> <AkBankTKBOWL plain> <listed bgm ids,comma> [csv out]"""
import glob, os, struct, sys
sys.path.insert(0, os.path.dirname(__file__))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import paklist
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY = b"=d6nw6YY6E#tI=6li6pI5CVaBC@fy%vR"

def bank_sounds(path):
    d = open(path, "rb").read(); o = 0; objs = {}
    while o + 8 <= len(d):
        tag, sz = d[o:o + 4], struct.unpack_from("<I", d, o + 4)[0]
        if tag == b"HIRC":
            s = o + 8; n = struct.unpack_from("<I", d, s)[0]; p = s + 4
            for _ in range(n):
                t = d[p]; z = struct.unpack_from("<I", d, p + 1)[0]; oid = struct.unpack_from("<I", d, p + 5)[0]
                objs[oid] = (t, d[p + 5:p + 5 + z]); p += 5 + z
        o += 8 + sz
    return objs

def header(fh, off, size):
    fh.seek(off); d = fh.read(min(size, 4096))
    if d[:4] != b"RIFF":
        n = len(d) // 16 * 16
        dec = Cipher(algorithms.AES(KEY), modes.ECB()).decryptor(); d = dec.update(d[:n]) + dec.finalize()
    if d[:4] != b"RIFF":
        return None
    info = {"codec": None, "ch": 0, "rate": 0, "samples": 0, "loop": None}
    o = 12
    while o + 8 <= len(d):
        tag, sz = d[o:o + 4], struct.unpack_from("<I", d, o + 4)[0]
        b = d[o + 8:o + 8 + sz]
        if tag == b"fmt " and len(b) >= 16:
            info["codec"], info["ch"], info["rate"] = struct.unpack_from("<HHI", b, 0)
            if info["codec"] == 0xFFFF and len(b) >= 0x1C:
                info["samples"] = struct.unpack_from("<I", b, 0x18)[0]
        elif tag == b"smpl" and len(b) >= 60:
            if struct.unpack_from("<I", b, 28)[0]:
                info["loop"] = struct.unpack_from("<II", b, 44)
        elif tag == b"data":
            if info["codec"] == 2 and info["ch"]:
                info["samples"] = sz // (36 * info["ch"]) * 64
            elif info["codec"] == 0xFFFE or info["codec"] == 1:
                info["samples"] = sz // (2 * max(1, info["ch"]))
            break
        o += 8 + sz + (sz & 1)
    return info

def main():
    paks, bgm_bank, bowl_bank, listed_ids = sys.argv[1:5]
    out = sys.argv[5] if len(sys.argv) > 5 else None
    used = set()
    for bank in (bgm_bank, bowl_bank):
        for t, b in bank_sounds(bank).values():
            if t == 2:
                used.add(struct.unpack_from("<IBII", b, 4)[2])
    files = {}
    order = sorted(glob.glob(os.path.join(paks, "pakchunk*_P.pak"))) + sorted(p for p in glob.glob(os.path.join(paks, "pakchunk*.pak")) if not p.endswith("_P.pak"))
    for pak in order:
        fh = open(pak, "rb")
        for name, off, size, usize, comp in paklist.entries(pak):
            if not name.endswith(".wem"):
                continue
            base = name.rsplit("/", 1)[-1][:-4]
            if not base.isdigit() or int(base) in files:
                continue
            fh.seek(off); hdr = 53 + (4 + 16 * 0 if comp else 0)
            if comp:
                files[int(base)] = (os.path.basename(pak), usize, None); continue
            files[int(base)] = (os.path.basename(pak), usize, header(fh, off + 53, size))
        fh.close()
    listed = set(int(x) for x in listed_ids.split(",") if x)
    rows = []
    for m, (pak, size, h) in files.items():
        if not h:
            continue
        rate = h["rate"] or 48000
        dur = h["samples"] / rate if h["samples"] else 0
        loop = h["loop"]
        rows.append((m, pak, size, h["codec"], h["ch"], dur, (loop[0] / rate, (loop[1] + 1) / rate) if loop else None, m in used, m in listed))
    looped = [r for r in rows if r[6]]
    print(f"{len(files)} wem files; {len(rows)} readable; {len(looped)} with loop points; {sum(1 for r in looped if r[7])} of those used by the BGM/Bowl banks")
    print("\nLOOPED, NOT USED BY THE BGM / BOWL BANKS (candidates):")
    for r in sorted((r for r in looped if not r[7]), key=lambda r: -r[5]):
        print(f"  {r[0]:>10}  {r[5]:6.1f} s  loop {r[6][0]:6.1f}..{r[6][1]:6.1f} s  ch {r[4]}  codec 0x{r[3]:04X}  {r[2]/1e6:5.1f} MB  {r[1]}")
    print("\nLOOPED, USED BY THE BANKS BUT NOT LISTED IN THE BROWSER:")
    for r in sorted((r for r in looped if r[7] and not r[8]), key=lambda r: -r[5]):
        print(f"  {r[0]:>10}  {r[5]:6.1f} s  loop {r[6][0]:6.1f}..{r[6][1]:6.1f} s  ch {r[4]}  codec 0x{r[3]:04X}  {r[1]}")
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write("media,pak,bytes,codec,channels,seconds,loop_start,loop_end,bank_used,listed\n")
            for r in sorted(rows):
                f.write(f"{r[0]},{r[1]},{r[2]},0x{r[3]:04X},{r[4]},{r[5]:.2f},{r[6][0] if r[6] else ''},{r[6][1] if r[6] else ''},{int(r[7])},{int(r[8])}\n")

main()
