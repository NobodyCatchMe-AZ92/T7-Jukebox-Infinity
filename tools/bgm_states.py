"""Map BGM_Selector / FinalRound state values to the media they play in AkBankBGM (plain dump). Dev tool.
  bgm_states.py <bank> <bgmtable.txt: '<id> BGM_Selector=<a> FinalRound=<b>' lines> [extra names ...]"""
import struct, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
def fnv(s):
    h = 2166136261
    for c in s.lower().encode():
        h = (h * 16777619) & 0xFFFFFFFF; h ^= c
    return h
d = open(sys.argv[1], "rb").read()
o = 0; hirc = None
while o + 8 <= len(d):
    tag, sz = d[o:o + 4], struct.unpack_from("<I", d, o + 4)[0]
    if tag == b"HIRC": hirc = (o + 8, sz)
    o += 8 + sz
s, _ = hirc; n = struct.unpack_from("<I", d, s)[0]; p = s + 4; objs = {}
for _ in range(n):
    t = d[p]; sz = struct.unpack_from("<I", d, p + 1)[0]; oid = struct.unpack_from("<I", d, p + 5)[0]
    objs[oid] = (t, d[p + 5:p + 5 + sz]); p += 5 + sz
names = {}
rows = []
for line in open(sys.argv[2], encoding="utf-8"):
    a = line.split()
    if len(a) < 3: continue
    sel, fin = a[1].split("=", 1)[1], a[2].split("=", 1)[1]
    rows.append((int(a[0]), sel, fin)); names[fnv(sel)] = sel; names[fnv(fin)] = fin
for x in sys.argv[3:]: names[fnv(x)] = x
# switch containers: find (stateID, count, child ids) runs
def switch_map(body):
    m = {}
    for i in range(4, len(body) - 8):
        sid = struct.unpack_from("<I", body, i)[0]
        if sid not in names: continue
        cnt = struct.unpack_from("<I", body, i + 4)[0]
        if not 0 < cnt <= 8 or i + 8 + 4 * cnt > len(body): continue
        kids = struct.unpack_from(f"<{cnt}I", body, i + 8)
        if all(k in objs for k in kids): m[names[sid]] = kids
    return m
def media(oid, depth=0):
    if oid not in objs or depth > 6: return []
    t, b = objs[oid]
    if t == 2: return [struct.unpack_from("<I", b, 9)[0]]
    out = []
    for i in range(4, len(b) - 3, 1):
        k = struct.unpack_from("<I", b, i)[0]
        if k in objs and k != oid and objs[k][0] in (2, 5, 6, 7) and k not in out:
            out.append(k)
    res = []
    for k in out: res += media(k, depth + 1)
    return list(dict.fromkeys(res))
sw = {oid: switch_map(b) for oid, (t, b) in objs.items() if t == 6}
sw = {k: v for k, v in sw.items() if v}
# selector -> container(s); then container keyed by FinalRound
sel_to = {}
for oid, m in sw.items():
    for nm, kids in m.items():
        sel_to.setdefault(nm, []).extend(kids)
def resolve(sel, fin):
    for c in sel_to.get(sel, []):
        if c in sw and fin in sw[c]:
            return [mm for k in sw[c][fin] for mm in media(k)]
    # FinalRound state may sit in a container not under that selector
    return None
for bid, sel, fin in rows:
    r = resolve(sel, fin)
    print(bid, sel, fin, "->", r if r else ("selector in bank" if sel in sel_to else "NOT IN BANK"))
print("\nstate names seen in switch containers but not in the table:")
seen = {nm for m in sw.values() for nm in m}
print(sorted(seen))
if "--sel" in sys.argv[3:] or True:
    print("\nselector children (all media below):")
    for nm in sorted({sel for _, sel, fin in rows if resolve(sel, fin) is None and sel in sel_to}):
        for c in sel_to.get(nm, []):
            print(" ", nm, c, "type", objs[c][0], "sub-states", sorted(sw.get(c, {}).keys()), "media", media(c))
