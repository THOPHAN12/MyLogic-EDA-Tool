# Project Structure Guide

- `cli/` – shell và lệnh
- `frontends/` – parser Verilog hợp nhất
- `core/optimization/` – strash, dce, cse, constprop, balance
- `core/synthesis/` – flow tổng hợp
- `integrations/yosys/` – tích hợp Yosys/ABC
- `core/simulation/` – arithmetic/logic/timing
- `core/vlsi_cad/` – bdd, sat, placement, routing, sta
- `core/technology_mapping/` – tech mapping
- `tools/` – analyzers, visualizers, converters
- `docs/` – tài liệu học thuật
- `examples/`, `tests/`, `outputs/`
