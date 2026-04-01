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


SYNTH_PATTERN = "*_syn.v"


def parse_width(range_text: str) -> int:
    if not range_text:
        return 1
    m = re.match(r"\[\s*(\d+)\s*:\s*(\d+)\s*\]", range_text)
    if not m:
        raise ValueError(f"Khong parse duoc do rong: {range_text}")
    msb = int(m.group(1))
    lsb = int(m.group(2))
    return abs(msb - lsb) + 1


def parse_module_and_ports(verilog_text: str) -> tuple[str, list[Port]]:
    module_match = re.search(r"\bmodule\s+([A-Za-z_]\w*)\s*\(", verilog_text)
    if not module_match:
        raise ValueError("Khong tim thay ten module")
    module_name = module_match.group(1)

    header_match = re.search(
        r"\bmodule\s+[A-Za-z_]\w*\s*\((.*?)\)\s*;",
        verilog_text,
        flags=re.S,
    )
    if not header_match:
        raise ValueError(f"Khong tim thay header module: {module_name}")

    header_text = header_match.group(1)
    ports: list[Port] = []
    for raw_line in header_text.splitlines():
        line = raw_line.strip().rstrip(",")
        if not line:
            continue
        m = re.match(
            r"^(input|output)\s+(?:reg\s+|wire\s+)?(\[[^\]]+\]\s+)?([A-Za-z_]\w*)$",
            line,
        )
        if not m:
            continue
        direction = m.group(1)
        range_text = (m.group(2) or "").strip()
        name = m.group(3)
        ports.append(
            Port(
                direction=direction,
                name=name,
                width=parse_width(range_text),
                range_text=range_text,
            )
        )
    if not ports:
        raise ValueError(f"Khong parse duoc cong I/O trong module: {module_name}")
    return module_name, ports


def build_tb(module_name: str, ports: list[Port], golden_rel: str, synth_rel: str) -> str:
    inputs = [p for p in ports if p.direction == "input"]
    outputs = [p for p in ports if p.direction == "output"]
    total_in_bits = sum(p.width for p in inputs)
    vector_count = (1 << total_in_bits) if total_in_bits <= 10 else 256
    compare_ops = "\n".join(
        [
            f'      if (gold_{p.name} !== syn_{p.name}) begin\n'
            f'        $display("FAIL {module_name}: vec=%0d {p.name} gold=%0h syn=%0h", vec_id, gold_{p.name}, syn_{p.name});\n'
            f"        $stop;\n"
            f"      end"
            for p in outputs
        ]
    )
    input_assign = "\n".join(
        [
            (
                f"      {p.name} = stim[{sum(x.width for x in inputs[:idx]) + p.width - 1}:{sum(x.width for x in inputs[:idx])}];"
                if p.width > 1
                else f"      {p.name} = stim[{sum(x.width for x in inputs[:idx])}];"
            )
            for idx, p in enumerate(inputs)
        ]
    )
    port_decl_inputs = "\n".join(
        [
            f"  reg {p.range_text + ' ' if p.range_text else ''}{p.name};"
            for p in inputs
        ]
    )
    port_decl_gold = "\n".join(
        [
            f"  wire {p.range_text + ' ' if p.range_text else ''}gold_{p.name};"
            for p in outputs
        ]
    )
    port_decl_syn = "\n".join(
        [
            f"  wire {p.range_text + ' ' if p.range_text else ''}syn_{p.name};"
            for p in outputs
        ]
    )
    connect_gold = ",\n".join(
        [f"    .{p.name}({p.name})" for p in inputs]
        + [f"    .{p.name}(gold_{p.name})" for p in outputs]
    )
    connect_syn = ",\n".join(
        [f"    .{p.name}({p.name})" for p in inputs]
        + [f"    .{p.name}(syn_{p.name})" for p in outputs]
    )

    return f"""`timescale 1ns/1ps

`define {module_name} {module_name}_golden
`include "{golden_rel}"
`undef {module_name}
`include "{synth_rel}"

module tb_{module_name}_synth_compare;
{port_decl_inputs}
{port_decl_gold}
{port_decl_syn}

  integer i;
  integer vec_id;
  reg [{total_in_bits - 1}:0] stim;

  {module_name}_golden u_golden (
{connect_gold}
  );

  {module_name} u_synth (
{connect_syn}
  );

  initial begin
    $display("=== BAT DAU SO SANH: {module_name} ===");
    for (i = 0; i < {vector_count}; i = i + 1) begin
      vec_id = i;
      stim = i;
{input_assign}
      #1;
{compare_ops}
      $display("OK {module_name}: vec=%0d", vec_id);
    end
    $display("PASS {module_name}: {vector_count} vector khop 100%%");
    $finish;
  end
endmodule
"""


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    outputs_dir = repo / "outputs"
    golden_dir = repo / "demo" / "CAN_DO"
    tb_dir = repo / "TESTBENCH" / "batch_synth"
    tb_dir.mkdir(parents=True, exist_ok=True)

    synth_files = sorted(outputs_dir.glob(SYNTH_PATTERN))
    if not synth_files:
        raise RuntimeError("Khong tim thay file *_syn.v trong outputs")

    generated = []
    for synth_file in synth_files:
        base_name = synth_file.name.replace("_syn.v", ".v")
        golden_file = golden_dir / base_name
        if not golden_file.exists():
            print(f"Bo qua (thieu golden): {synth_file.name}")
            continue

        module_name, ports = parse_module_and_ports(synth_file.read_text(encoding="utf-8"))
        tb_text = build_tb(
            module_name=module_name,
            ports=ports,
            golden_rel=f"../../demo/CAN_DO/{golden_file.name}",
            synth_rel=f"../../outputs/{synth_file.name}",
        )
        tb_path = tb_dir / f"tb_{module_name}_synth_compare.v"
        tb_path.write_text(tb_text, encoding="utf-8")
        generated.append(tb_path.name)

    do_lines = [
        "vlib work",
        "transcript on",
    ]
    for tb_name in generated:
        top = tb_name.replace(".v", "")
        do_lines.append(f"vlog TESTBENCH/batch_synth/{tb_name}")
        do_lines.append(f"vsim -c work.{top} -do \"run -all; quit -f\"")

    do_path = tb_dir / "run_all_synth_compare.do"
    do_path.write_text("\n".join(do_lines) + "\n", encoding="utf-8")

    print("Da tao cac file testbench:")
    for name in generated:
        print(f" - {name}")
    print(f"Da tao file chay batch: {do_path}")


if __name__ == "__main__":
    main()
