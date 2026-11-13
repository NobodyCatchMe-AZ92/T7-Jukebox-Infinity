"""Explore the music hierarchy of AkBankBGM.bnk (Wwise bank v118) for the loop preview (dev tool).

HIRC object types used: 0x0A music segment, 0x0B music track, 0x0C music switch container, 0x0D music playlist.
Heuristics (no full v118 schema): a track's playlist items are (trackID u32, sourceID u32, playAt f64, beginTrim f64,
endTrim f64, srcDuration f64); a segment's markers are (id u32, position f64 [, name]) after its duration f64;
the entry / exit cue markers have the well-known ids 43573010 / 1539036744.

  bgm_hierarchy.py <bank> [media id ...]
"""
import struct
import sys

ENTRY, EXIT = 43573010, 1539036744


def hirc(d):
    o = 0
    while o + 8 <= len(d):
        tag, size = d[o:o + 4], struct.unpack_from("<I", d, o + 4)[0]
        if tag == b"HIRC":
            n = struct.unpack_from("<I", d, o + 8)[0]
            p = o + 12
            for _ in range(n):
                t, sz = d[p], struct.unpack_from("<I", d, p + 1)[0]
                oid = struct.unpack_from("<I", d, p + 5)[0]
                yield t, oid, d[p + 5:p + 5 + sz]
                p += 5 + sz
        o += 8 + size


def plausible(x):
    return 0.0 <= x < 3.6e6


def track_items(body, src):
    """playlist items of a track that play media `src`: (playAt, beginTrim, endTrim, srcDuration) in ms"""
    out = []
    key = struct.pack("<I", src)
    i = body.find(key)
    while i >= 0:
        if i >= 4 and i + 4 + 32 <= len(body):
            vals = struct.unpack_from("<4d", body, i + 4)
            if all(-3.6e6 < v < 3.6e6 for v in vals) and plausible(vals[3]) and vals[3] > 0:
                out.append(vals)
        i = body.find(key, i + 1)
    return out


def markers(body):
    res = {}
    for mid in (ENTRY, EXIT):
        k = struct.pack("<I", mid)
        i = body.find(k)
        if i >= 0 and i + 12 <= len(body):
            res[mid] = struct.unpack_from("<d", body, i + 4)[0]
    return res


def main():
    d = open(sys.argv[1], "rb").read()
    objs = list(hirc(d))
    by_type = {}
    for t, oid, b in objs:
        by_type.setdefault(t, []).append((oid, b))
    print({hex(k): len(v) for k, v in sorted(by_type.items())})
    want = [int(x) for x in sys.argv[2:]]
    tracks = by_type.get(0x0B, [])
    segs = by_type.get(0x0A, [])
    for media in want:
        print(f"\n== media {media}")
        for tid, tb in tracks:
            items = track_items(tb, media)
            if not items and struct.pack("<I", media) not in tb:
                continue
            print(f"  track {tid} (body {len(tb)} bytes) items {[tuple(round(v, 1) for v in it) for it in items]}")
            for sid, sb in segs:
                if struct.pack("<I", tid) in sb[4:]:
                    m = markers(sb)
                    print(f"    in segment {sid}: entry {m.get(ENTRY)} exit {m.get(EXIT)} (ms)")
                    for t2 in (0x0D, 0x0C):
                        for pid, pb in by_type.get(t2, []):
                            if struct.pack("<I", sid) in pb[4:]:
                                print(f"      referenced by {'playlist' if t2 == 0x0D else 'switch'} {pid}")


if __name__ == "__main__":
    main()
