"""Hack assembler (two-pass) - Niriksha Tiwari, Roll No. 2501730353, K = 53.
Usage: python assembler.py Box.asm   ->  writes Box.hack
Duplicate labels are rejected (K mod 3 = 2)."""
import sys, re

COMP = {'0':'101010','1':'111111','-1':'111010','D':'001100','A':'110000','!D':'001101',
        '!A':'110001','-D':'001111','-A':'110011','D+1':'011111','A+1':'110111','D-1':'001110',
        'A-1':'110010','D+A':'000010','D-A':'010011','A-D':'000111','D&A':'000000','D|A':'010101'}
JMP = {'':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}

def assemble(src):
    sym = {'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4,'SCREEN':16384,'KBD':24576}
    sym.update({f'R{i}': i for i in range(16)})
    prog, seen = [], set()
    for n, l in enumerate(src.splitlines(), 1):          # pass 1: labels
        l = re.sub(r'//.*', '', l).replace(' ', '').strip()
        if not l: continue
        m = re.fullmatch(r'\((.+)\)', l)
        if m:
            if m[1] in seen: raise SystemExit(f'Error line {n}: duplicate label ({m[1]})')
            seen.add(m[1]); sym[m[1]] = len(prog)
        else:
            prog.append(l)
    nxt, out = 16, []
    for l in prog:                                        # pass 2: code
        if l[0] == '@':
            v = l[1:]
            if not v.isdigit():
                if v not in sym: sym[v] = nxt; nxt += 1
                v = sym[v]
            out.append(format(int(v), '016b'))
        else:
            dest, comp = l.split('=') if '=' in l else ('', l)
            comp, _, j = comp.partition(';')
            a = '1' if 'M' in comp else '0'
            c = comp.replace('M', 'A')
            c = {'A+D':'D+A','A&D':'D&A','A|D':'D|A'}.get(c, c)
            d = ''.join('1' if x in dest else '0' for x in 'ADM')
            out.append('111' + a + COMP[c] + d + JMP[j])
    return out

if __name__ == '__main__':
    f = sys.argv[1]
    open(f.rsplit('.', 1)[0] + '.hack', 'w').write('\n'.join(assemble(open(f).read())) + '\n')
