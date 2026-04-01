from __future__ import annotations

from typing import Dict, Callable, List, TYPE_CHECKING

if TYPE_CHECKING:
    from cli.mylogic_shell import MyLogicShell


def _cmd_help(shell: "MyLogicShell", parts: List[str] | None = None) -> None:
    print("=== ENHANCED MYLOGIC EDA TOOL COMMANDS ===")
    print()
    print("File Operations:")
    print("  read <file>           - Load a .v file (auto-exports JSON to outputs/)")
    print("  stats                 - Enhanced circuit statistics")
    print("  vectors               - Detailed vector width analysis")
    print("  nodes                 - Detailed node information")
    print("  wires                 - Detailed wire analysis")
    print("  modules               - Module instantiation details")
    print("  export [file]         - Export netlist to JSON file (manual export)")
    print("  dump / dump_ast       - Dump netlist structure as AST tree (like Yosys)")
    print("  dump_synth            - Dump synthesized netlist (AIG->netlist) as cells/cones")
    print()
    print("Logic Synthesis:")
    print("  synthesis             - Netlist -> AIG")
    print("  strash                - Structural hashing")
    print("  dce [level]          - Dead code elimination")
    print("  cse                  - Common subexpression elimination")
    print("  constprop            - Constant propagation")
    print("  balance              - Logic balancing")
    print("  optimize             - AIG optimization (Strash, DCE, CSE, ConstProp, Balance)")
    print("  export_aig [flags]   - Export current AIG as synthesized JSON/Verilog")
    print("  techmap [strategy]   - Technology mapping (area/delay/balanced)")
    print("  complete_flow [strategy] [library] - Full flow")
    print("  aig <op>              - AIG (create/strash/convert/stats)")
    print()
    print("Utility: stats, vectors, nodes, wires, modules, export, history, clear, help, exit")


def _cmd_exit(shell: "MyLogicShell", parts: List[str] | None = None) -> None:
    print("Goodbye.")
    raise SystemExit(0)


def _cmd_clear(shell: "MyLogicShell", parts: List[str] | None = None) -> None:
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def _cmd_history(shell: "MyLogicShell", parts: List[str] | None = None) -> None:
    if not shell.history:
        print("No commands in history.")
        return
    print("Command history:")
    for i, cmd in enumerate(shell.history[-10:], 1):
        print(f"  {i:2d}. {cmd}")


def register(shell: "MyLogicShell") -> Dict[str, Callable]:
    return {
        "help": lambda parts=None: _cmd_help(shell, parts),
        "exit": lambda parts=None: _cmd_exit(shell, parts),
        "clear": lambda parts=None: _cmd_clear(shell, parts),
        "history": lambda parts=None: _cmd_history(shell, parts),
    }

