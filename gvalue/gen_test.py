import sys
from pathlib import Path

def parse_gen(text: str):
    lines = [l.rstrip() for l in text.splitlines() if l.strip() != ""]
    # header
    first = lines[0].split()
    natoms = int(first[0])
    mode = first[1]  # 'S' or 'C'
    elems = lines[1].split()

    atom_lines = lines[2:2+natoms]
    atoms = []
    for l in atom_lines:
        parts = l.split()
        idx = int(parts[0])
        sid = int(parts[1])
        x, y, z = map(float, parts[2:5])
        atoms.append((idx, sid, x, y, z))

    if mode.upper() == "S":
        tail = lines[2+natoms:2+natoms+4]
        origin = list(map(float, tail[0].split()))
        a = list(map(float, tail[1].split()))
        b = list(map(float, tail[2].split()))
        c = list(map(float, tail[3].split()))
        return natoms, mode, elems, atoms, origin, a, b, c
    else:
        # 非週期情況不在這次需求
        raise ValueError("Only 'S' mode (periodic supercell) is handled here.")

def write_gen(natoms, mode, elems, atoms, origin, a, b, c):
    out = []
    out.append(f"{natoms} {mode}")
    out.append(" ".join(elems))
    for i, sid, x, y, z in atoms:
        out.append(f"{i:6d} {sid:3d} {x: .10E} {y: .10E} {z: .10E}")
    out.append(f"{origin[0]: .10E} {origin[1]: .10E} {origin[2]: .10E}")
    out.append(f"{a[0]: .10E} {a[1]: .10E} {a[2]: .10E}")
    out.append(f"{b[0]: .10E} {b[1]: .10E} {b[2]: .10E}")
    out.append(f"{c[0]: .10E} {c[1]: .10E} {c[2]: .10E}")
    return "\n".join(out) + "\n"

def add_vec(p, v):
    return (p[0] + v[0], p[1] + v[1], p[2] + v[2])

def main():
    if len(sys.argv) != 6:
        print("Usage: gen_supercell.py in.gen out.gen nx ny nz")
        sys.exit(2)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    nx, ny, nz = map(int, sys.argv[3:6])
    if nx <= 0 or ny <= 0 or nz <= 0:
        raise ValueError("nx, ny, nz must be positive integers.")

    natoms, mode, elems, atoms, origin, a, b, c = parse_gen(in_path.read_text())

    # 原本晶格向量
    ax, ay, az = a
    bx, by, bz = b
    cx, cy, cz = c

    # 新晶格向量（簡單情況：用整數倍放大）
    a2 = [ax * nx, ay * nx, az * nx]
    b2 = [bx * ny, by * ny, bz * ny]
    c2 = [cx * nz, cy * nz, cz * nz]

    # 生成平移向量：i*a + j*b + k*c
    shifts = []
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                shifts.append([ax*i + bx*j + cx*k,
                               ay*i + by*j + cy*k,
                               az*i + bz*j + cz*k])

    new_atoms = []
    new_idx = 1
    for shift in shifts:
        for (_, sid, x, y, z) in atoms:
            x2, y2, z2 = add_vec((x, y, z), shift)
            new_atoms.append((new_idx, sid, x2, y2, z2))
            new_idx += 1

    natoms2 = natoms * nx * ny * nz
    out_path.write_text(write_gen(natoms2, mode, elems, new_atoms, origin, a2, b2, c2))
    print(f"Wrote {natoms2} atoms to {out_path}")

if __name__ == "__main__":
    main()

