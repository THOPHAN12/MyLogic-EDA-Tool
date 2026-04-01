from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Port:
    direction: str
    name: str
    width: int
    range_text: str


def parse_module_and_ports(path: Path) -> tuple[str, list[Port]]:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"\bmodule\s+([A-Za-z_]\w*)\s*\(", text)
    if not m:
        raise ValueError(f"Khong tim thay module trong {path.name}")
    module_name = m.group(1)

    h = re.search(r"\bmodule\s+[A-Za-z_]\w*\s*\((.*?)\)\s*;", text, flags=re.S)
    if not h:
        raise ValueError(f"Khong tim thay header port trong {path.name}")

    ports: list[Port] = []
    for raw in h.group(1).splitlines():
        line = raw.strip().rstrip(",")
        if not line:
            continue
        mm = re.match(
            r"^(input|output)\s+(?:reg\s+|wire\s+)?(\[[^\]]+\]\s+)?([A-Za-z_]\w*)$",
            line,
        )
        if not mm:
            continue
        rng = (mm.group(2) or "").strip()
        width = 1
        if rng:
            wm = re.match(r"\[\s*(\d+)\s*:\s*(\d+)\s*\]", rng)
            if wm:
                width = abs(int(wm.group(1)) - int(wm.group(2))) + 1
        ports.append(Port(mm.group(1), mm.group(3), width, rng))
    if not ports:
        raise ValueError(f"Khong parse duoc ports trong {path.name}")
    return module_name, ports


def make_tb_text(synth_file: Path, bak_file: Path, tb_name: str) -> str:
    synth_mod, ports = parse_module_and_ports(synth_file)
    bak_mod, _ = parse_module_and_ports(bak_file)

    inputs = [p for p in ports if p.direction == "input"]
    outputs = [p for p in ports if p.direction == "output"]
    in_bits = sum(p.width for p in inputs)
    vectors = 1 << in_bits

    decl_inputs = "\n".join(
        f"  reg {p.range_text + ' ' if p.range_text else ''}{p.name};" for p in inputs
    )
    decl_gold = "\n".join(
        f"  wire {p.range_text + ' ' if p.range_text else ''}gold_{p.name};" for p in outputs
    )
    decl_syn = "\n".join(
        f"  wire {p.range_text + ' ' if p.range_text else ''}syn_{p.name};" for p in outputs
    )

    conn_gold = ",\n".join(
        [f"    .{p.name}({p.name})" for p in inputs] +
        [f"    .{p.name}(gold_{p.name})" for p in outputs]
    )
    conn_syn = ",\n".join(
        [f"    .{p.name}({p.name})" for p in inputs] +
        [f"    .{p.name}(syn_{p.name})" for p in outputs]
    )

    assigns = []
    offset = 0
    for p in inputs:
        if p.width == 1:
            assigns.append(f"      {p.name} = stim[{offset}];")
        else:
            assigns.append(f"      {p.name} = stim[{offset + p.width - 1}:{offset}];")
        offset += p.width
    input_assign = "\n".join(assigns)

    checks = "\n".join(
        [
            f"      if (gold_{p.name} !== syn_{p.name}) begin\n"
            f"        $display(\"FAIL {tb_name}: vec=%0d {p.name} gold=%0h syn=%0h\", vec_id, gold_{p.name}, syn_{p.name});\n"
            f"        $stop;\n"
            f"      end"
            for p in outputs
        ]
    )

    return f"""`timescale 1ns/1ps

`define {bak_mod} {bak_mod}_bak
`include "{bak_file.name}"
`undef {bak_mod}
`include "{synth_file.name}"

module tb_{tb_name};
{decl_inputs}
{decl_gold}
{decl_syn}

  integer i;
  integer vec_id;
  reg [{in_bits - 1}:0] stim;

  {bak_mod}_bak u_bak (
{conn_gold}
  );

  {synth_mod} u_synth (
{conn_syn}
  );

  initial begin
    $display("=== BAT DAU TEST {tb_name} ===");
    for (i = 0; i < {vectors}; i = i + 1) begin
      vec_id = i;
      stim = i;
{input_assign}
      #1;
{checks}
      $display("OK {tb_name}: vec=%0d", vec_id);
    end
    $display("PASS {tb_name}: {vectors} vector khop");
    $finish;
  end
endmodule
"""


def main() -> None:
    tb_dir = Path(r"D:\KHOA_LUAN_TOT_NGHIEP\Mylogic\TESTBENCH")
    synth_files = sorted(tb_dir.glob("*_syn.v"))

    created: list[str] = []
    skipped: list[str] = []
    for synth in synth_files:
        tb_file = tb_dir / f"tb_{synth.name}"
        if tb_file.exists():
            skipped.append(tb_file.name)
            continue
        bak = tb_dir / f"{synth.name}.bak"
        if not bak.exists():
            skipped.append(f"{tb_file.name} (thieu .bak)")
            continue
        tb_name = synth.stem
        tb_text = make_tb_text(synth, bak, tb_name)
        tb_file.write_text(tb_text, encoding="utf-8")
        created.append(tb_file.name)

    print("Da tao:")
    for n in created:
        print(f" - {n}")
    print("Da bo qua:")
    for n in skipped:
        print(f" - {n}")


if __name__ == "__main__":
    main()
