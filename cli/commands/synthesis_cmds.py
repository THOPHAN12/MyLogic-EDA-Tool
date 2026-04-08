from __future__ import annotations

import os
import re
from typing import Callable, Dict, List, Optional, Tuple, TYPE_CHECKING

_VERILOG_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*$")


def _is_legal_verilog_identifier(name: str) -> bool:
    return bool(name and _VERILOG_IDENTIFIER_RE.match(name))


def _ensure_verilog_file_extension(path: str) -> str:
    """Nếu đường dẫn không có .v/.sv, thêm .v (ví dụ outputs/01_combinational_gates)."""
    _, ext = os.path.splitext(path)
    if ext.lower() in (".v", ".sv"):
        return path
    return path + ".v"


def _resolve_synthesized_module_name(output_path: str, netlist: Dict) -> str:
    """
    Tên module trong file Verilog phải là identifier hợp lệ.
    Stem bắt đầu bằng số (01_...) không hợp lệ → dùng tên module từ netlist + _syn.
    """
    base_name = netlist.get("name") or "design"
    file_stem = os.path.splitext(os.path.basename(output_path))[0]
    for suffix in ("_syn", "_opt", "_mapped"):
        if file_stem.endswith(suffix):
            return f"{base_name}{suffix}"
    if _is_legal_verilog_identifier(file_stem):
        return file_stem
    return f"{base_name}_syn"

if TYPE_CHECKING:
    from cli.mylogic_shell import MyLogicShell

# Chiến lược techmap cố định area_optimal (CLI không nhận delay/balanced).
_DEPRECATED_TECHMAP_STRATEGY_WORDS = frozenset({"area", "delay", "balanced"})


def _library_token_from_positionals(positionals: List[str]) -> Optional[str]:
    """Bỏ qua các từ khóa strategy cũ (area/delay/balanced); trả về token thư viện đầu tiên."""
    i = 0
    while i < len(positionals) and positionals[i].lower() in _DEPRECATED_TECHMAP_STRATEGY_WORDS:
        i += 1
    if i >= len(positionals):
        return None
    return positionals[i]


def _parse_techmap_cli_parts(parts: List[str]) -> Tuple[Optional[str], bool]:
    """
    Trả về (library_file_or_type | None, merge_standard_library).
    Cờ --pure-library / --no-standard-merge: không gộp create_standard_library() khi techmap.
    """
    merge_standard = True
    positionals: List[str] = []
    i = 1
    while i < len(parts):
        p = parts[i]
        if p in ("--pure-library", "--no-standard-merge"):
            merge_standard = False
            i += 1
            continue
        if p in ("--json", "-j", "--verilog", "-v"):
            i += 1
            if i < len(parts) and not parts[i].startswith("-"):
                i += 1
            continue
        positionals.append(p)
        i += 1
    return _library_token_from_positionals(positionals), merge_standard


def _export_synthesized_netlist_json(
    shell: "MyLogicShell",
    synthesized_netlist: Dict,
    output_path: Optional[str] = None,
    *,
    aig_stage: Optional[str] = None,
) -> None:
    import json
    import os
    from datetime import datetime

    if not output_path:
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        if shell.filename:
            base_name = os.path.splitext(os.path.basename(shell.filename))[0]
            output_path = os.path.join(output_dir, f"{base_name}_syn.json")
        else:
            output_path = os.path.join(output_dir, "synthesized.json")

    meta = {
        "tool": "MyLogic EDA Tool v2.0.0",
        "export_time": datetime.now().isoformat(),
        "source_file": shell.filename or "unknown",
        "version": "2.0.0",
        "auto_exported": True,
        "export_type": "synthesized_netlist",
    }
    if aig_stage:
        meta["aig_stage"] = aig_stage
    export_data = {
        "metadata": meta,
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
    from core.export import netlist_to_verilog

    if not output_path:
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        if shell.filename:
            base_name = os.path.splitext(os.path.basename(shell.filename))[0]
            output_path = os.path.join(output_dir, f"{base_name}_syn.v")
        else:
            output_path = os.path.join(output_dir, "synthesized.v")
    else:
        output_path = _ensure_verilog_file_extension(output_path)

    # Preserve vector widths from original netlist if available, so port widths are correct.
    orig_attrs = (shell.current_netlist or {}).get("attrs", {}) or {}
    orig_vw = orig_attrs.get("vector_widths", {}) or {}
    if orig_vw:
        synthesized_netlist.setdefault("attrs", {})
        synthesized_netlist["attrs"].setdefault("vector_widths", {})
        # Do not overwrite widths already present in synthesized netlist.
        for k, v in orig_vw.items():
            synthesized_netlist["attrs"]["vector_widths"].setdefault(k, v)

    module_name = _resolve_synthesized_module_name(output_path, synthesized_netlist)
    verilog_text = netlist_to_verilog(synthesized_netlist, module_name=module_name)
    out_dir = os.path.dirname(output_path) if os.path.dirname(output_path) else "."
    if out_dir and out_dir != "." and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(verilog_text)
    print(f"[OK] Exported synthesized Verilog to: {output_path} (module {module_name})")


def _export_mapped_netlist_json(
    shell: "MyLogicShell",
    mapped_netlist: Dict,
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
            output_path = os.path.join(output_dir, f"{base_name}_mapped.json")
        else:
            output_path = os.path.join(output_dir, "mapped.json")

    export_data = {
        "metadata": {
            "tool": "MyLogic EDA Tool v2.0.0",
            "export_time": datetime.now().isoformat(),
            "source_file": shell.filename or "unknown",
            "version": "2.0.0",
            "auto_exported": True,
            "export_type": "technology_mapped_netlist",
        },
        "netlist": mapped_netlist,
    }

    out_dir = os.path.dirname(output_path) if os.path.dirname(output_path) else "."
    if out_dir and out_dir != "." and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Exported technology-mapped netlist to: {output_path}")


def _export_mapped_verilog(
    shell: "MyLogicShell",
    mapped_netlist: Dict,
    output_path: Optional[str] = None,
) -> None:
    from core.export import netlist_to_verilog

    if not output_path:
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        if shell.filename:
            base_name = os.path.splitext(os.path.basename(shell.filename))[0]
            output_path = os.path.join(output_dir, f"{base_name}_mapped.v")
        else:
            output_path = os.path.join(output_dir, "mapped.v")
    else:
        output_path = _ensure_verilog_file_extension(output_path)

    orig_attrs = (shell.current_netlist or {}).get("attrs", {}) or {}
    orig_vw = orig_attrs.get("vector_widths", {}) or {}
    if orig_vw:
        mapped_netlist.setdefault("attrs", {})
        mapped_netlist["attrs"].setdefault("vector_widths", {})
        for k, v in orig_vw.items():
            mapped_netlist["attrs"]["vector_widths"].setdefault(k, v)

    rtl_base = mapped_netlist.get("name") or "design"
    module_name = f"{rtl_base}_mapped"
    if shell.filename:
        stem = os.path.splitext(os.path.basename(shell.filename))[0]
        if _is_legal_verilog_identifier(f"{stem}_mapped"):
            module_name = f"{stem}_mapped"

    verilog_text = netlist_to_verilog(mapped_netlist, module_name=module_name)
    out_dir = os.path.dirname(output_path) if os.path.dirname(output_path) else "."
    if out_dir and out_dir != "." and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(verilog_text)
    print(f"[OK] Exported technology-mapped Verilog to: {output_path} (module {module_name})")


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

        # Optional export JSON: synthesis --export | --json | -o | -j [output_path]
        if any(p in ("--export", "-o", "--json", "-j") for p in parts[1:]):
            out_path = None
            for i, p in enumerate(parts[1:], start=1):
                if p in ("--export", "-o", "--json", "-j"):
                    # allow: synthesis --export OR synthesis --export <path>
                    if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                        out_path = parts[i + 1]
                    break
            synthesized_netlist = aig_to_netlist(
                shell.current_aig,
                shell.current_netlist,
                simplify_and_with_const1=False,
            )
            _export_synthesized_netlist_json(
                shell, synthesized_netlist, out_path, aig_stage="post_synthesis"
            )

        # Optional export Verilog: synthesis --verilog [output_path]
        if any(p in ("--verilog", "-v") for p in parts[1:]):
            out_path = None
            for i, p in enumerate(parts[1:], start=1):
                if p in ("--verilog", "-v"):
                    if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                        out_path = parts[i + 1]
                    break
            synthesized_netlist = aig_to_netlist(
                shell.current_aig,
                shell.current_netlist,
                simplify_and_with_const1=False,
            )
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

        # Optional: optimize --verilog [output_path] / optimize --json [output_path]
        parts = parts or []
        if any(p in ("--verilog", "-v", "--json", "-j") for p in parts[1:]):
            import os

            forwarded = ["export_aig", *parts[1:]]

            def _maybe_inject_default(flag: str, default_suffix: str) -> None:
                if flag not in forwarded:
                    return
                i = forwarded.index(flag)
                has_path = (i + 1 < len(forwarded)) and (not str(forwarded[i + 1]).startswith("-"))
                if has_path:
                    return
                base = os.path.splitext(os.path.basename(shell.filename or "design"))[0]
                default_path = os.path.join("outputs", f"{base}{default_suffix}")
                forwarded.insert(i + 1, default_path)

            # If user requested export but didn't provide a path, avoid overwriting *_syn.*
            _maybe_inject_default("--verilog", "_opt.v")
            _maybe_inject_default("-v", "_opt.v")
            _maybe_inject_default("--json", "_opt.json")
            _maybe_inject_default("-j", "_opt.json")

            _cmd_export_aig(shell, forwarded, _aig_stage="post_optimize")
    except ImportError:
        print("[ERROR] Optimization module not available")
    except Exception as e:
        print(f"[ERROR] Optimization failed: {e}")
        import traceback
        traceback.print_exc()


def _cmd_export_aig(
    shell: "MyLogicShell",
    parts: Optional[List[str]] = None,
    *,
    _aig_stage: Optional[str] = None,
) -> None:
    """
    Export synthesized netlist from the *current* AIG (after optimize/strash/etc).
    This does NOT re-run synthesis; it uses shell.current_aig directly.
    """
    if not shell.current_aig:
        print("[ERROR] No AIG available. Run 'synthesis' first.")
        return
    if not shell.current_netlist:
        print("[ERROR] No original netlist available (shell.current_netlist is empty).")
        return

    try:
        from core.synthesis.aig import aig_to_netlist
        from typing import Optional as _Optional

        synthesized_netlist = aig_to_netlist(shell.current_aig, shell.current_netlist)

        parts = parts or []
        if not parts or all(p not in ("--verilog", "-v", "--json", "-j") for p in parts[1:]):
            # Default: export both
            _export_synthesized_netlist_json(
                shell, synthesized_netlist, None, aig_stage=_aig_stage
            )
            _export_synthesized_verilog(shell, synthesized_netlist, None)
            return

        out_json: _Optional[str] = None
        out_v: _Optional[str] = None
        for i, p in enumerate(parts[1:], start=1):
            if p in ("--json", "-j"):
                if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                    out_json = parts[i + 1]
                break
        for i, p in enumerate(parts[1:], start=1):
            if p in ("--verilog", "-v"):
                if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                    out_v = parts[i + 1]
                break

        if out_json is not False and any(p in ("--json", "-j") for p in parts[1:]):
            _export_synthesized_netlist_json(
                shell, synthesized_netlist, out_json, aig_stage=_aig_stage
            )
        if out_v is not False and any(p in ("--verilog", "-v") for p in parts[1:]):
            _export_synthesized_verilog(shell, synthesized_netlist, out_v)

    except ImportError:
        print("[ERROR] Export from AIG failed: core.synthesis.aig missing")
    except Exception as e:
        print(f"[ERROR] Export from AIG failed: {e}")
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
    parts = parts or []
    if len(parts) >= 2 and parts[1].lower() in ("-h", "--help", "help"):
        print("Usage: techmap [library_file|library_type] [options]")
        print("  Mapping strategy is fixed: area_optimal (area).")
        print("Library types: asic, sky130, sky130_ls, skywater, fpga, ...")
        print("  Corner: MYLOGIC_SKY130_CORNER (hd: tt_025C_1v80; ls: tt_100C_1v80 default)")
        print("Options: [--pure-library|--no-standard-merge]")
        print("         [--json [output_path]] [--verilog [output_path]]")
        print("Example: techmap sky130 --pure-library --verilog outputs/mapped.v")
        print("Note: Requires AIG (run synthesis / optimize first).")
        return
    library_path, merge_standard_library = _parse_techmap_cli_parts(parts)
    strategy = "area_optimal"

    if not shell.current_aig:
        print("[ERROR] No AIG available. Run 'synthesis' first to convert Netlist -> AIG.")
        return

    try:
        from core.technology_mapping.technology_mapping import (
            techmap,
            create_standard_library,
            load_library_from_file,
            convert_mapped_logic_network_to_netlist,
        )
        import os

        print("[INFO] Running technology mapping (strategy: area_optimal, fixed).")
        print(f"[INFO] Input AIG: {shell.current_aig.count_nodes()} nodes, {shell.current_aig.count_and_nodes()} AND nodes")

        library = None
        if library_path:
            valid_types = [
                "asic", "fpga", "fpga_common", "anlogic", "gowin", "ice40", "intel",
                "lattice", "xilinx", "sky130", "sky130_ls", "skywater",
            ]
            if library_path.lower() in valid_types:
                library = shell._try_load_default_library(library_path.lower())
            elif os.path.exists(library_path):
                library = load_library_from_file(library_path)
            else:
                print(f"[WARNING] Library file not found: {library_path}")

        if library is None:
            print("[WARNING] No library loaded, using standard library")
            library = create_standard_library()

        if not merge_standard_library:
            print("[INFO] Techmap: pure library mode (no merge with internal standard_cells).")

        results = techmap(
            shell.current_aig,
            library,
            strategy,
            merge_standard_library=merge_standard_library,
        )
        mapper = results.get("_mapper")
        aig_for_mapping = results.get("_aig")
        mapped_netlist = None
        if mapper and aig_for_mapping and shell.current_netlist:
            mapped_netlist = convert_mapped_logic_network_to_netlist(
                mapper,
                aig_for_mapping,
                shell.current_netlist,
            )
            if shell.filename:
                import os as _os
                base_name = _os.path.splitext(_os.path.basename(shell.filename))[0]
                mapped_netlist["name"] = f"{base_name}_mapped"

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

        if mapper:
            mapper.print_mapping_report(results)

        out_json: Optional[str] = None
        out_v: Optional[str] = None
        for i, p in enumerate(parts[1:], start=1):
            if p in ("--json", "-j"):
                if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                    out_json = parts[i + 1]
                else:
                    out_json = None
                break
        for i, p in enumerate(parts[1:], start=1):
            if p in ("--verilog", "-v"):
                if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                    out_v = parts[i + 1]
                else:
                    out_v = None
                break

        if mapped_netlist and any(p in ("--json", "-j") for p in parts[1:]):
            _export_mapped_netlist_json(shell, mapped_netlist, out_json)
        if mapped_netlist and any(p in ("--verilog", "-v") for p in parts[1:]):
            _export_mapped_verilog(shell, mapped_netlist, out_v)

        print("[OK] Technology mapping completed")
    except ImportError:
        print("[ERROR] Technology mapping module not available")
    except Exception as e:
        print(f"[ERROR] Technology mapping failed: {e}")


def _cmd_complete_flow(shell: "MyLogicShell", parts: List[str]) -> None:
    parts = parts or []
    if len(parts) >= 2 and parts[1].lower() in ("-h", "--help", "help"):
        print("Usage: complete_flow [library_path_or_type] [options]")
        print("  Techmap strategy is fixed: area_optimal.")
        print("  library: optional (asic, sky130, sky130_ls, skywater, fpga, ... or path)")
        print("  options: --pure-library | --no-standard-merge")
        print("Example: complete_flow sky130 --pure-library")
        return
    if not shell.current_netlist:
        print("[ERROR] No netlist loaded. Use 'read <file>' first.")
        return

    positional_args = [p for p in parts[1:] if not p.startswith("--") and not p.startswith("-")]
    techmap_library_path = _library_token_from_positionals(positional_args)
    techmap_merge_standard_library = (
        "--pure-library" not in parts[1:] and "--no-standard-merge" not in parts[1:]
    )

    try:
        from core.complete_flow import run_complete_flow
        from core.technology_mapping.technology_mapping import load_library_from_file
        import os
        from core.synthesis.aig import aig_to_netlist

        print("=" * 70)
        print("COMPLETE FLOW: Synthesis -> Optimization -> Technology Mapping")
        print("=" * 70)
        print("Techmap strategy: area_optimal (fixed).")
        if not techmap_merge_standard_library:
            print("Techmap: pure library mode (no merge with internal standard_cells).")
        print()

        library = None
        if techmap_library_path:
            valid_types = [
                "asic", "sky130", "sky130_ls", "skywater", "fpga", "fpga_common",
                "anlogic", "gowin", "ice40", "intel", "lattice", "xilinx",
            ]
            if techmap_library_path.lower() in valid_types:
                library = shell._try_load_default_library(techmap_library_path.lower())
            elif os.path.exists(techmap_library_path):
                library = load_library_from_file(techmap_library_path)
            else:
                print(f"[WARNING] Library path not found: {techmap_library_path}")

        results = run_complete_flow(
            shell.current_netlist,
            techmap_library=library,
            enable_optimization=True,
            enable_techmap=True,
            techmap_merge_standard_library=techmap_merge_standard_library,
        )

        if results["optimization"].get("enabled") and results["optimization"].get("aig"):
            shell.current_aig = results["optimization"]["aig"]
        elif results["synthesis"].get("aig"):
            shell.current_aig = results["synthesis"]["aig"]

        # Optional export: complete_flow ... --export | --json | -o | -j [output_path]
        if shell.current_aig and any(
            p in ("--export", "-o", "--json", "-j") for p in parts[1:]
        ):
            out_path = None
            for i, p in enumerate(parts[1:], start=1):
                if p in ("--export", "-o", "--json", "-j"):
                    if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                        out_path = parts[i + 1]
                    break
            synthesized_netlist = aig_to_netlist(shell.current_aig, shell.current_netlist)
            _cf_stage = (
                "post_optimize"
                if results["optimization"].get("enabled")
                else "post_synthesis"
            )
            _export_synthesized_netlist_json(
                shell, synthesized_netlist, out_path, aig_stage=_cf_stage
            )

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
        "export_aig": lambda parts=None: _cmd_export_aig(shell, parts),
        "dce": lambda parts: _cmd_dce(shell, parts),
        "aig": lambda parts: _cmd_aig(shell, parts),
        "techmap": lambda parts: _cmd_techmap(shell, parts),
        "complete_flow": lambda parts: _cmd_complete_flow(shell, parts),
        "workflow": lambda parts: _cmd_complete_flow(shell, parts),
    }

