"""Decode small inline UE4 (4.14) Texture2D uassets (DXT1/DXT5/B8G8R8A8, mip 0) to RGBA. Dev helper.
  ue_tex.py sheet <outpng> <uasset ...>   -> contact sheet with labels by index (printed)"""
import struct, sys, zlib, os
def png(path, w, h, rgba):
    raw = b"".join(b"\0" + bytes(rgba[y * w * 4:(y + 1) * w * 4]) for y in range(h))
    def ch(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)) + ch(b"IDAT", zlib.compress(raw)) + ch(b"IEND", b""))
def c565(c): return [((c >> 11) & 31) * 255 // 31, ((c >> 5) & 63) * 255 // 63, (c & 31) * 255 // 31]
def dxt(data, w, h, five):
    out = bytearray(w * h * 4); p = 0
    for by in range(0, h, 4):
        for bx in range(0, w, 4):
            if five:
                a0, a1 = data[p], data[p + 1]; ab = int.from_bytes(data[p + 2:p + 8], "little"); p += 8
                al = [a0, a1] + ([((6 - i) * a0 + i * a1) // 6 for i in range(1, 7)] if a0 > a1 else [((4 - i) * a0 + i * a1) // 4 for i in range(1, 5)] + [0, 255])
            c0, c1, bits = struct.unpack_from("<HHI", data, p); p += 8
            k0, k1 = c565(c0), c565(c1)
            if c0 > c1 or five: cols = [k0, k1, [(2 * a + b) // 3 for a, b in zip(k0, k1)], [(a + 2 * b) // 3 for a, b in zip(k0, k1)]]
            else: cols = [k0, k1, [(a + b) // 2 for a, b in zip(k0, k1)], [0, 0, 0]]
            for i in range(16):
                x, y = bx + i % 4, by + i // 4
                if x >= w or y >= h: continue
                ci = (bits >> (2 * i)) & 3; c = cols[ci]
                a = al[(ab >> (3 * i)) & 7] if five else (0 if (c0 <= c1 and ci == 3) else 255)
                o = (y * w + x) * 4; out[o:o + 4] = bytes(c + [a])
    return out
def decode(path):
    d = open(path, "rb").read()
    for fmt in (b"PF_DXT5", b"PF_DXT1", b"PF_B8G8R8A8"):
        k = d.rfind(fmt + b"\0")
        if k > 0 and struct.unpack_from("<i", d, k - 4)[0] == len(fmt) + 1: break
    else: return None
    sx, sy = struct.unpack_from("<ii", d, k - 16)
    q = k + len(fmt) + 1 + 16  # firstmip, nummips, cooked, bulk flags
    cnt, dsk, off = struct.unpack_from("<iiq", d, q); q += 16
    data = d[q:q + dsk]
    if fmt == b"PF_B8G8R8A8":
        rgba = bytearray(sx * sy * 4)
        for i in range(sx * sy): b, g, r, a = data[4 * i:4 * i + 4]; rgba[4 * i:4 * i + 4] = bytes((r, g, b, a))
        return sx, sy, rgba
    return sx, sy, dxt(data, sx, sy, fmt == b"PF_DXT5")
if __name__ == "__main__":
    out, files = sys.argv[2], sys.argv[3:]
    imgs = []
    for f in files:
        r = decode(f)
        print(len(imgs), os.path.basename(f), r[:2] if r else "?")
        if r: imgs.append(r)
    cell = 80; cols = 12; rows = (len(imgs) + cols - 1) // cols
    W, H = cols * cell, rows * cell; sheet = bytearray([60, 60, 60, 255] * W * H)
    for n, (w, h, px) in enumerate(imgs):
        s = max(w, h) / (cell - 8); s = max(s, 1)
        ox, oy = (n % cols) * cell + 4, (n // cols) * cell + 4
        for y in range(int(h / s)):
            for x in range(int(w / s)):
                o = (int(y * s) * w + int(x * s)) * 4; r, g, b, a = px[o:o + 4]
                t = ((oy + y) * W + ox + x) * 4; bg = sheet[t:t + 3]
                sheet[t:t + 3] = bytes((r * a + c * (255 - a)) // 255 for r, c in zip((r, g, b), bg))
    png(out, W, H, sheet)
