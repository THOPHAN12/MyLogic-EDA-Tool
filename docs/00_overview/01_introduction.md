# MyLogic EDA Tool – Introduction

## Purpose
MyLogic là nền tảng EDA học thuật phục vụ học tập và nghiên cứu: từ Verilog RTL tới tối ưu, mô phỏng, và tích hợp Yosys/ABC.

## Scope
- Frontend: `frontends/unified_verilog.py`
- Optimization: `core/optimization/`
- Synthesis: `core/synthesis/` và `integrations/yosys/`
- Simulation: `core/simulation/`
- VLSI CAD: `core/vlsi_cad/`
- Technology Mapping: `core/technology_mapping/`

## High-level Dataflow
1) Parse Verilog → netlist (inputs/outputs/nodes/wires, attrs)
2) Optimize (strash, dce, cse, constprop, balance)
3) Simulate (arithmetic/logic/timing)
4) Map/Analyze (techmap, placement, routing, STA, SAT/BDD)
5) Export/Visualize

## Audience
Sinh viên, nhà nghiên cứu, giảng viên, và nhà phát triển EDA.
