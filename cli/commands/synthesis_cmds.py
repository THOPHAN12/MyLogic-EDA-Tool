from __future__ import annotations

from typing import Callable, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from cli.mylogic_shell import MyLogicShell


def _export_synthesized_netlist_json(
    shell: "MyLogicShell",
    synthesized_netlist: Dict,
    output_path: Optional[str] = None,
) -> None:
    import json
    import os
    from datetime import datetime

    if not output_path:
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        if shell.filename:
            base_name = os.path.splitext(os.path.basename(shell.filename))[0]
            output_path = os.path.join(output_dir, f"{base_name}_synthesized.json")
        else:
            output_path = os.path.join(output_dir, "synthesized.json")

    export_data = {
        "metadata": {
            "tool": "MyLogic EDA Tool v2.0.0",
            "export_time": datetime.now().isoformat(),
            "source_file": shell.filename or "unknown",
            "version": "2.0.0",
            "auto_exported": True,
            "export_type": "synthesized_netlist",
        },
        "netlist": synthesized_netlist,
    }

    out_dir = os.path.dirname(output_path) if os.path.dirname(output_path) else "."
    if out_dir and out_dir != "." and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Exported synthesized netlist to: {output_path}")


def _export_synthesized_verilog(
    shell: "MyLogicShell",
    synthesized_netlist: Dict,
    output_path: Optional[str] = None,
) -> None:
    import os
    from core.export import netlist_to_verilog

    if not output_path:
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        if shell.filename:
            base_name = os.path.splitext(os.path.basename(shell.filename))[0]
            output_path = os.path.join(output_dir, f"{base_name}_synthesized.v")
        else:
            output_path = os.path.join(output_dir, "synthesized.v")

    # Preserve vector widths from original netlist if available, so port widths are correct.
    orig_attrs = (shell.current_netlist or {}).get("attrs", {}) or {}
    orig_vw = orig_attrs.get("vector_widths", {}) or {}
    if orig_vw:
        synthesized_netlist.setdefault("attrs", {})
        synthesized_netlist["attrs"].setdefault("vector_widths", {})
        # Do not overwrite widths already present in synthesized netlist.
        for k, v in orig_vw.items():
            synthesized_netlist["attrs"]["vector_widths"].setdefault(k, v)

    verilog_text = netlist_to_verilog(synthesized_netlist, module_name=synthesized_netlist.get("name"))
    out_dir = os.path.dirname(output_path) if os.path.dirname(output_path) else "."
    if out_dir and out_dir != "." and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(verilog_text)
    print(f"[OK] Exported synthesized Verilog to: {output_path}")


def _cmd_strash(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    if not shell.current_netlist:
        print("[ERROR] No netlist loaded. Use 'read <file>' first.")
        return
    try:
        from core.synthesis.strash import StrashOptimizer
        print("[INFO] Running Structural Hashing optimization...")
        original_nodes = len(shell.current_netlist.get("nodes", {}))
        optimizer = StrashOptimizer()
        shell.current_netlist = optimizer.optimize(shell.current_netlist)
        optimized_nodes = len(shell.current_netlist.get("nodes", {}))
        print("[OK] Structural Hashing completed!")
        print(f"  Original: {original_nodes} nodes")
        print(f"  Optimized: {optimized_nodes} nodes")
        print(f"  Removed: {original_nodes - optimized_nodes} nodes")
    except ImportError:
        print("[ERROR] Strash module not available")
    except Exception as e:
        print(f"[ERROR] Structural Hashing failed: {e}")


def _cmd_cse(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    if not shell.current_netlist:
        print("[ERROR] No netlist loaded. Use 'read <file>' first.")
        return
    try:
        from core.optimization.cse import CSEOptimizer
        import logging
        cse_logger = logging.getLogger("core.optimization.cse")
        cse_logger.setLevel(logging.ERROR)
        cse_logger.propagate = False
        print("[INFO] Running Common Subexpression Elimination...")
        original_nodes = len(shell.current_netlist.get("nodes", {}))
        optimizer = CSEOptimizer()
        shell.current_netlist = optimizer.optimize(shell.current_netlist)
        optimized_nodes = len(shell.current_netlist.get("nodes", {}))
        print("[OK] CSE optimization completed!")
        print(f"  Original: {original_nodes} nodes")
        print(f"  Optimized: {optimized_nodes} nodes")
        print(f"  Removed: {original_nodes - optimized_nodes} nodes")
    except ImportError:
        print("[ERROR] CSE module not available")
    except Exception as e:
        print(f"[ERROR] CSE optimization failed: {e}")


def _cmd_constprop(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    if not shell.current_netlist:
        print("[ERROR] No netlist loaded. Use 'read <file>' first.")
        return
    try:
        from core.optimization.constprop import ConstPropOptimizer
        import logging
        cp_logger = logging.getLogger("core.optimization.constprop")
        cp_logger.setLevel(logging.ERROR)
        cp_logger.propagate = False
        print("[INFO] Running Constant Propagation...")
        original_nodes = len(shell.current_netlist.get("nodes", {}))
        optimizer = ConstPropOptimizer()
        shell.current_netlist = optimizer.optimize(shell.current_netlist)
        optimized_nodes = len(shell.current_netlist.get("nodes", {}))
        print("[OK] Constant Propagation completed!")
        print(f"  Original: {original_nodes} nodes")
        print(f"  Optimized: {optimized_nodes} nodes")
        print(f"  Simplified: {original_nodes - optimized_nodes} nodes")
    except ImportError:
        print("[ERROR] ConstProp module not available")
    except Exception as e:
        print(f"[ERROR] Constant Propagation failed: {e}")


def _cmd_balance(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    if not shell.current_netlist:
        print("[ERROR] No netlist loaded. Use 'read <file>' first.")
        return
    try:
        from core.optimization.balance import BalanceOptimizer
        import logging
        bal_logger = logging.getLogger("core.optimization.balance")
        bal_logger.setLevel(logging.ERROR)
        bal_logger.propagate = False
        print("[INFO] Running Logic Balancing...")
        original_nodes = len(shell.current_netlist.get("nodes", {}))
        optimizer = BalanceOptimizer()
        shell.current_netlist = optimizer.optimize(shell.current_netlist)
        optimized_nodes = len(shell.current_netlist.get("nodes", {}))
        print("[OK] Logic Balancing completed!")
        print(f"  Original: {original_nodes} nodes")
        print(f"  Balanced: {optimized_nodes} nodes")
        print(f"  Added: {optimized_nodes - original_nodes} nodes")
    except ImportError:
        print("[ERROR] Balance module not available")
    except Exception as e:
        print(f"[ERROR] Logic Balancing failed: {e}")


def _cmd_synthesis(shell: "MyLogicShell", parts: List[str]) -> None:
    if not shell.current_netlist:
        print("[ERROR] No netlist loaded. Use 'read <file>' first.")
        return
    try:
        from core.synthesis.synthesis_flow import synthesize
        from core.synthesis.aig import aig_to_netlist
        print("[INFO] Running Synthesis: Netlist -> AIG conversion...")
        nodes_data = shell.current_netlist.get("nodes", {})
        if isinstance(nodes_data, (dict, list)):
            original_nodes = len(nodes_data)
        else:
            original_nodes = 0
        shell.current_aig = synthesize(shell.current_netlist)
        print("[OK] Synthesis completed!")
        print(f"  Netlist nodes: {original_nodes}")
        print(f"  AIG nodes: {shell.current_aig.count_nodes()}")
        print(f"  AIG AND nodes: {shell.current_aig.count_and_nodes()}")
        print(f"  Primary inputs: {len(shell.current_aig.pis)}")
        print(f"  Primary outputs: {len(shell.current_aig.pos)}")
        print("[INFO] Next step: Run 'optimize' to optimize AIG")

        # Optional export JSON: synthesis --export [output_path]
        if any(p in ("--export", "-o") for p in parts[1:]):
            out_path = None
            for i, p in enumerate(parts[1:], start=1):
                if p in ("--export", "-o"):
                    # allow: synthesis --export OR synthesis --export <path>
                    if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                        out_path = parts[i + 1]
                    break
            synthesized_netlist = aig_to_netlist(shell.current_aig, shell.current_netlist)
            _export_synthesized_netlist_json(shell, synthesized_netlist, out_path)

        # Optional export Verilog: synthesis --verilog [output_path]
        if any(p in ("--verilog", "-v") for p in parts[1:]):
            out_path = None
            for i, p in enumerate(parts[1:], start=1):
                if p in ("--verilog", "-v"):
                    if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                        out_path = parts[i + 1]
                    break
            synthesized_netlist = aig_to_netlist(shell.current_aig, shell.current_netlist)
            _export_synthesized_verilog(shell, synthesized_netlist, out_path)
    except ImportError:
        print("[ERROR] Synthesis module not available")
    except Exception as e:
        print(f"[ERROR] Synthesis failed: {e}")
        import traceback
        traceback.print_exc()


def _cmd_optimize(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    if not shell.current_aig:
        print("[ERROR] No AIG available. Run 'synthesis' first to convert Netlist -> AIG.")
        return
    try:
        from core.optimization.optimization_flow import optimize
        print("[INFO] Running AIG Optimization...")
        original_nodes = shell.current_aig.count_nodes()
        shell.current_aig = optimize(shell.current_aig)
        final_nodes = shell.current_aig.count_nodes()
        reduction = original_nodes - final_nodes
        print("[OK] AIG Optimization completed!")
        print(f"  Original AIG nodes: {original_nodes}")
        print(f"  Optimized AIG nodes: {final_nodes}")
        if original_nodes > 0:
            print(f"  Total reduction: {reduction} nodes ({(reduction/original_nodes)*100:.1f}%)")
    except ImportError:
        print("[ERROR] Optimization module not available")
    except Exception as e:
        print(f"[ERROR] Optimization failed: {e}")
        import traceback
        traceback.print_exc()


def _cmd_dce(shell: "MyLogicShell", parts: List[str]) -> None:
    if not parts or len(parts) < 2:
        print("Usage: dce <level>")
        print("Levels: basic, advanced, aggressive")
        return
    level = parts[1].lower()
    if level not in ["basic", "advanced", "aggressive"]:
        print("Invalid DCE level. Use: basic, advanced, or aggressive")
        return
    if not shell.current_netlist:
        print("[ERROR] No netlist loaded. Use 'read <file>' first.")
        return
    try:
        from core.optimization.dce import DCEOptimizer
        print(f"[INFO] Running DCE optimization (level: {level})...")
        original_nodes = len(shell.current_netlist.get("nodes", {}))
        original_wires = len(shell.current_netlist.get("wires", []))
        optimizer = DCEOptimizer()
        shell.current_netlist = optimizer.optimize(shell.current_netlist, level)
        optimized_nodes = len(shell.current_netlist.get("nodes", {}))
        optimized_wires = len(shell.current_netlist.get("wires", []))
        print("[OK] DCE optimization completed!")
        print(f"  Original: {original_nodes} nodes, {original_wires} wires")
        print(f"  Optimized: {optimized_nodes} nodes, {optimized_wires} wires")
        print(f"  Removed: {original_nodes - optimized_nodes} nodes, {original_wires - optimized_wires} wires")
    except ImportError:
        print("[ERROR] DCE module not available")
    except Exception as e:
        print(f"[ERROR] DCE optimization failed: {e}")


def _cmd_techmap(shell: "MyLogicShell", parts: List[str]) -> None:
    if not parts or len(parts) < 2:
        print("Usage: techmap <strategy> [library_file|library_type]")
        print("Strategies: area, delay, balanced")
        print("Note: Techmap requires AIG from synthesis or optimization.")
        return
    if not shell.current_aig:
        print("[ERROR] No AIG available. Run 'synthesis' first to convert Netlist -> AIG.")
        return

    strategy = parts[1].lower()
    library_path = parts[2] if len(parts) > 2 else None

    strategy_map = {"area": "area_optimal", "delay": "delay_optimal", "balanced": "balanced"}
    strategy = strategy_map.get(strategy, strategy)

    try:
        from core.technology_mapping.technology_mapping import techmap, create_standard_library, load_library_from_file
        import os

        print(f"[INFO] Running technology mapping with {strategy} strategy...")
        print(f"[INFO] Input AIG: {shell.current_aig.count_nodes()} nodes, {shell.current_aig.count_and_nodes()} AND nodes")

        library = None
        if library_path:
            valid_types = ["asic", "fpga", "fpga_common", "anlogic", "gowin", "ice40", "intel", "lattice", "xilinx", "sky130"]
            if library_path.lower() in valid_types:
                library = shell._try_load_default_library(library_path.lower())
            elif os.path.exists(library_path):
                library = load_library_from_file(library_path)
            else:
                print(f"[WARNING] Library file not found: {library_path}")

        if library is None:
            print("[WARNING] No library loaded, using standard library")
            library = create_standard_library()

        results = techmap(shell.current_aig, library, strategy)
        print("\n" + "=" * 60)
        print("TECHNOLOGY MAPPING REPORT")
        print("=" * 60)
        print(f"Mapping Strategy: {results['strategy']}")
        print(f"Total Nodes: {results['total_nodes']}")
        print(f"Mapped Nodes: {results['mapped_nodes']}")
        print(f"Mapping Success Rate: {results['mapping_success_rate']*100:.1f}%")
        if "total_area" in results:
            print(f"Total Area: {results['total_area']:.2f}")
        if "total_delay" in results:
            print(f"Total Delay: {results['total_delay']:.2f}")
        print(f"Library: {results.get('library_name', 'N/A')}")
        print("=" * 60)
        print("[OK] Technology mapping completed")
    except ImportError:
        print("[ERROR] Technology mapping module not available")
    except Exception as e:
        print(f"[ERROR] Technology mapping failed: {e}")


def _cmd_complete_flow(shell: "MyLogicShell", parts: List[str]) -> None:
    if not parts:
        print("Usage: complete_flow [techmap_strategy] [techmap_library]")
        print("  techmap_strategy: area, delay, balanced (default: area)")
        print("  techmap_library: library path or type (optional, default: auto)")
        return
    if not shell.current_netlist:
        print("[ERROR] No netlist loaded. Use 'read <file>' first.")
        return

    positional_args = [p for p in parts[1:] if not p.startswith("--") and not p.startswith("-")]
    techmap_strategy = positional_args[0].lower() if len(positional_args) > 0 else "area"
    techmap_strategy_map = {"area": "area_optimal", "delay": "delay_optimal", "balanced": "balanced"}
    techmap_strategy = techmap_strategy_map.get(techmap_strategy, techmap_strategy)

    techmap_library_path = positional_args[1] if len(positional_args) > 1 else None

    try:
        from core.complete_flow import run_complete_flow
        from core.technology_mapping.technology_mapping import load_library_from_file
        import os
        from core.synthesis.aig import aig_to_netlist

        print("=" * 70)
        print("COMPLETE FLOW: Synthesis -> Optimization -> Technology Mapping")
        print("=" * 70)
        print(f"Techmap strategy: {techmap_strategy}\n")

        library = None
        if techmap_library_path:
            valid_types = ["asic", "sky130", "fpga", "fpga_common", "anlogic", "gowin", "ice40", "intel", "lattice", "xilinx"]
            if techmap_library_path.lower() in valid_types:
                library = shell._try_load_default_library(techmap_library_path.lower())
            elif os.path.exists(techmap_library_path):
                library = load_library_from_file(techmap_library_path)
            else:
                print(f"[WARNING] Library path not found: {techmap_library_path}")

        results = run_complete_flow(
            shell.current_netlist,
            techmap_strategy=techmap_strategy,
            techmap_library=library,
            enable_optimization=True,
            enable_techmap=True,
        )

        if results["optimization"].get("enabled") and results["optimization"].get("aig"):
            shell.current_aig = results["optimization"]["aig"]
        elif results["synthesis"].get("aig"):
            shell.current_aig = results["synthesis"]["aig"]

        # Optional export: complete_flow ... --export [output_path]
        if shell.current_aig and any(p in ("--export", "-o") for p in parts[1:]):
            out_path = None
            for i, p in enumerate(parts[1:], start=1):
                if p in ("--export", "-o"):
                    if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                        out_path = parts[i + 1]
                    break
            synthesized_netlist = aig_to_netlist(shell.current_aig, shell.current_netlist)
            _export_synthesized_netlist_json(shell, synthesized_netlist, out_path)

        print("\n" + "=" * 70)
        print("COMPLETE FLOW RESULTS SUMMARY")
        print("=" * 70)
        synth_stats = results["synthesis"]["stats"]
        print("\n[1] Synthesis:")
        print(f"    Netlist nodes: {synth_stats['netlist_nodes']}")
        print(f"    AIG nodes: {synth_stats['aig_nodes']}")
        print(f"    AIG AND nodes: {synth_stats['aig_and_nodes']}")

        if results["optimization"].get("enabled") and results["optimization"].get("stats"):
            opt_stats = results["optimization"]["stats"]
            print("\n[2] Optimization:")
            print(f"    Before: {opt_stats['nodes_before']} nodes")
            print(f"    After: {opt_stats['nodes_after']} nodes")
            print(f"    Reduction: {opt_stats['reduction']} nodes ({opt_stats['reduction_percent']:.1f}%)")
        else:
            print("\n[2] Optimization: SKIPPED")

        if results["techmap"].get("enabled") and results["techmap"].get("results"):
            tm = results["techmap"]["results"]
            print("\n[3] Technology Mapping:")
            print(f"    Mapped: {tm['mapped_nodes']}/{tm['total_nodes']} nodes")
            print(f"    Success rate: {tm['mapping_success_rate']*100:.1f}%")
        else:
            print("\n[3] Technology Mapping: SKIPPED")

        print("=" * 70)
        print("[OK] Complete flow finished successfully!")
        print("=" * 70)
    except ImportError as e:
        print(f"[ERROR] Complete flow module not available: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"[ERROR] Complete flow failed: {e}")
        import traceback
        traceback.print_exc()


def _cmd_aig(shell: "MyLogicShell", parts: List[str]) -> None:
    if not parts or len(parts) < 2:
        print("Usage: aig <operation>")
        print("Operations: create, strash, convert, stats")
        return
    op = parts[1].lower()
    try:
        from core.synthesis.aig import AIG
        if op == "create":
            aig = AIG()
            a = aig.create_pi("a"); b = aig.create_pi("b"); c = aig.create_pi("c")
            ab = aig.create_and(a, b)
            f = aig.create_or(ab, c)
            aig.add_po(f)
            print("AIG Creation Example:")
            for k, v in aig.get_statistics().items():
                print(f"  {k}: {v}")
        elif op == "strash":
            aig = AIG()
            a = aig.create_pi("a"); b = aig.create_pi("b")
            ab1 = aig.create_and(a, b)
            ab2 = aig.create_and(a, b)
            print("AIG Structural Hashing Example:")
            print(f"  ab1 node_id: {ab1.node_id}")
            print(f"  ab2 node_id: {ab2.node_id}")
            print(f"  Same node (structural hashing): {ab1 == ab2}")
            print(f"  Total nodes: {aig.count_nodes()}")
        elif op == "convert":
            aig = AIG()
            a = aig.create_pi("a"); b = aig.create_pi("b"); c = aig.create_pi("c")
            ab = aig.create_and(a, b)
            f = aig.create_or(ab, c)
            aig.add_po(f)
            print("AIG to Verilog Conversion:")
            print(aig.to_verilog("example_aig"))
        elif op == "stats":
            aig = AIG()
            a = aig.create_pi("a"); b = aig.create_pi("b"); c = aig.create_pi("c")
            ab = aig.create_and(a, b)
            ac = aig.create_and(a, c)
            f = aig.create_or(ab, ac)
            aig.add_po(f)
            print("AIG Statistics:")
            for k, v in aig.get_statistics().items():
                print(f"  {k}: {v}")
        else:
            print("Invalid AIG operation. Use: create, strash, convert, or stats")
    except ImportError:
        print("[ERROR] AIG module not available")
    except Exception as e:
        print(f"[ERROR] AIG operation failed: {e}")


def register(shell: "MyLogicShell") -> Dict[str, Callable]:
    return {
        "strash": lambda parts=None: _cmd_strash(shell, parts),
        "cse": lambda parts=None: _cmd_cse(shell, parts),
        "constprop": lambda parts=None: _cmd_constprop(shell, parts),
        "balance": lambda parts=None: _cmd_balance(shell, parts),
        "synthesis": lambda parts: _cmd_synthesis(shell, parts),
        "optimize": lambda parts=None: _cmd_optimize(shell, parts),
        "dce": lambda parts: _cmd_dce(shell, parts),
        "aig": lambda parts: _cmd_aig(shell, parts),
        "techmap": lambda parts: _cmd_techmap(shell, parts),
        "complete_flow": lambda parts: _cmd_complete_flow(shell, parts),
        "workflow": lambda parts: _cmd_complete_flow(shell, parts),
    }

