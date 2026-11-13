"""Static RE helper for TekkenGame-Win64-Shipping.exe (read-only).

Usage:  py -I tools/t7re.py <cmd> [args]      (needs: pip install capstone pefile numpy)
  The exe path can be set with the environment variable T7_EXE.
  str <text> [w]        file offsets + RVAs of an ascii (or utf-16 with 'w') string
  xref <rva>            code locations referencing <rva> (rip-relative), with their function
  dis <rva> [n]         disassemble n instructions from rva (default 60)
  fn <rva>              disassemble the whole function containing rva (.pdata bounds)
  ptr <rva>             places in data sections holding the VA of rva (vtables, tables)
"""
import bisect
import re
import struct
import sys

import os
import capstone
import pefile

EXE = os.environ.get("T7_EXE", r"C:/Program Files (x86)/Steam/steamapps/common/TEKKEN 7/TekkenGame/Binaries/Win64/TekkenGame-Win64-Shipping.exe")
pe = pefile.PE(EXE, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXCEPTION"]])
data = pe.__data__
BASE = pe.OPTIONAL_HEADER.ImageBase
text = next(s for s in pe.sections if s.Name.startswith(b".text"))
TXT_RVA, TXT_OFF, TXT_SZ = text.VirtualAddress, text.PointerToRawData, text.Misc_VirtualSize
code = data[TXT_OFF:TXT_OFF + TXT_SZ]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = False

funcs = sorted((e.struct.BeginAddress, e.struct.EndAddress) for e in pe.DIRECTORY_ENTRY_EXCEPTION)
starts = [f[0] for f in funcs]


def func_of(rva):
    i = bisect.bisect_right(starts, rva) - 1
    if i >= 0 and funcs[i][0] <= rva < funcs[i][1]:
        return funcs[i]
    return None


def off2rva(off):
    return pe.get_rva_from_offset(off)


def rva2off(rva):
    return pe.get_offset_from_rva(rva)


def find_str(s, wide=False):
    pat = s.encode("utf-16le") if wide else s.encode()
    return [(m.start(), off2rva(m.start())) for m in re.finditer(re.escape(pat), data)]


def xrefs(target):
    """rip-relative disp32 references: scan every position whose disp32 + next-ip == target.
    Checks common encodings: [opcode..modrm disp32] with instruction end = pos+4 (+imm size)."""
    # disp at offset p; instr end = p + 4 + imm; target = TXT_RVA + p + 4 + imm + disp
    import numpy as np
    out = []
    hits = set()
    for shift in range(4):
        n = (len(code) - shift) // 4
        vals = np.frombuffer(code, dtype="<i4", count=n, offset=shift).astype(np.int64)
        pos = shift + 4 * np.arange(n, dtype=np.int64)
        for imm in (0, 1, 4):
            for k in np.nonzero(TXT_RVA + pos + 4 + imm + vals == target)[0]:
                hits.add((int(pos[k]), imm))
    for p, imm in sorted(hits):
        if True:
            if True:
                    # validate: decode an instruction starting a few bytes before p
                    for back in range(2, 8):
                        st = p - back
                        ins = next(md.disasm(code[st:st + 16], TXT_RVA + st), None)
                        if ins and ins.size == back + 4 + imm:
                            out.append((TXT_RVA + st, f"{ins.mnemonic} {ins.op_str}"))
                            break
    return sorted(set(out))


def dis(rva, n=60, end=None):
    off = rva - TXT_RVA
    stop = (end - TXT_RVA) if end else off + 16 * n
    k = 0
    for ins in md.disasm(code[off:stop], rva):
        print(f"  {ins.address:08X}  {ins.mnemonic:8s} {ins.op_str}{note(ins)}")
        k += 1
        if not end and k >= n:
            break


def note(ins):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", ins.op_str)
    if not m:
        return ""
    t = ins.address + ins.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16))
    s = peek_str(t)
    return f"   ; -> {t:#x}{(' ' + repr(s)) if s else ''}"


def peek_str(rva):
    try:
        off = rva2off(rva)
    except Exception:
        return None
    b = data[off:off + 120]
    m = re.match(rb"[ -~]{4,}", b)
    if m:
        return m.group().decode()
    m = re.match(rb"(?:[ -~]\x00){3,}", b)
    if m:
        return m.group().decode("utf-16le")
    return None


def ptrs(rva):
    va = struct.pack("<Q", BASE + rva)
    return [off2rva(m.start()) for m in re.finditer(re.escape(va), data)]


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "str":
        for off, r in find_str(args[0], len(args) > 1):
            print(f"off {off:#x} rva {r:#x}")
    elif cmd == "xref":
        for a, t in xrefs(int(args[0], 16)):
            f = func_of(a)
            print(f"{a:#x}  {t}   fn {f[0]:#x}" if f else f"{a:#x}  {t}")
    elif cmd == "dis":
        dis(int(args[0], 16), int(args[1]) if len(args) > 1 else 60)
    elif cmd == "fn":
        f = func_of(int(args[0], 16))
        print(f"function {f[0]:#x}..{f[1]:#x}")
        dis(f[0], end=f[1])
    elif cmd == "ptr":
        for r in ptrs(int(args[0], 16)):
            print(f"{r:#x}")


def calls(target):
    """E8/E9 rel32 calls/jumps to target."""
    import numpy as np
    out = []
    for shift in range(4):
        n = (len(code) - shift) // 4
        vals = np.frombuffer(code, dtype="<i4", count=n, offset=shift).astype(np.int64)
        pos = shift + 4 * np.arange(n, dtype=np.int64)
        for k in np.nonzero(TXT_RVA + pos + 4 + vals == target)[0]:
            p = int(pos[k]) - 1
            if p >= 0 and code[p] in (0xE8, 0xE9):
                out.append(TXT_RVA + p)
    return sorted(out)


def near(rva, k=5):
    i = bisect.bisect_right(starts, rva)
    return funcs[max(0, i - k):i + k]


if __name__ == "__main__" and sys.argv[1] in ("calls", "near"):
    if sys.argv[1] == "calls":
        for a in calls(int(sys.argv[2], 16)):
            f = func_of(a)
            print(f"{a:#x}   fn {f[0]:#x}" if f else f"{a:#x}")
    else:
        for f in near(int(sys.argv[2], 16)):
            print(f"{f[0]:#x}..{f[1]:#x}")
