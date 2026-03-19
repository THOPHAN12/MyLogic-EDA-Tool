from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class CheckResult:
    path: str
    ok: bool
    expected_ok: bool
    stage: str
    error: str | None = None


def _is_expected_fail(path: str) -> bool:
    p = path.replace("\\", "/").lower()
    # These examples currently run end-to-end (even if out-of-scope conceptually).
    allow_ok = (
        "/examples/08_module_instantiation/test_named_ports.v",
        "/examples/16_technology_mapping/test_techmap.v",
        "/examples/tests_verilog/yosys_case_bit_slices.v",
        "/examples/tests_verilog/yosys_case_named_ports.v",
        "/examples/tests_verilog/yosys_case_ordered_ports.v",
    )
    if any(p.endswith(x) for x in allow_ok):
        return False
    # Files that intentionally contain syntax/strict-mode violations.
    if "/examples/99_edge_cases/syntax_errors/" in p:
        return True
    if p.endswith("/examples/99_edge_cases/implicit_wire_should_fail.v"):
        return True
    if p.endswith("/examples/99_edge_cases/default_nettype_none_should_fail.v"):
        return True
    # This example intentionally contains a syntax typo (double comma) for teaching.
    if p.endswith("/examples/01_parameters/test_parameters.v"):
        return True

    # Sequential always blocks are out-of-scope for strict combinational batch (may parse, but not required here).
    if p.endswith("/examples/02_always_blocks/test_always_sequential.v"):
        return True

    # Replication example is out-of-scope for strict combinational subset
    if p.endswith("/examples/05_bit_manipulation/test_replication.v"):
        return True

    # Module instantiation / techmap / yosys regression corpus are out-of-scope
    if p.endswith("/examples/08_module_instantiation/test_named_ports.v"):
        return True
    if p.endswith("/examples/08_module_instantiation/test_ordered_ports.v"):
        return True
    if p.endswith("/examples/08_module_instantiation/test_named_ports.v"):
        return True
    if p.endswith("/examples/16_technology_mapping/test_techmap.v"):
        return True
    if "/examples/tests_verilog/" in p:
        return True

    # Sequential DFF isolation example is outside strict combinational subset
    if p.endswith("/examples/99_edge_cases/dff_isolation.v"):
        return True

    # Out-of-scope examples for current MyLogic subset (combinational-focused learning):
    # - module instantiation, generate, case-heavy regression corpus
    # - functions/tasks
    # - memory arrays / array indexing
    # - technology mapping demos
    # - shift/mul/div/mod operators not yet bit-blasted here
    out_of_scope_dirs = (
        "/examples/03_generate_blocks/",
        "/examples/04_case_statements/",
        "/examples/06_memory_arrays/",
        "/examples/07_functions_tasks/",
        "/examples/08_module_instantiation/",
        "/examples/14_shift_operations/",
        "/examples/15_comprehensive/",
        "/examples/16_technology_mapping/",
        "/examples/tests_verilog/",
    )
    if any(d in p for d in out_of_scope_dirs):
        return True

    # Arithmetic demo includes mul/div/mod which are not supported.
    if "/examples/10_arithmetic/" in p:
        return True
    # Optimization demo includes a * operator in an unused wire (mul unsupported).
    if p.endswith("/examples/09_optimization/unoptimized.v"):
        return True

    return False


def _walk_verilog_files(examples_dir: str) -> List[str]:
    out: List[str] = []
    for root, _dirs, files in os.walk(examples_dir):
        for fn in files:
            if fn.lower().endswith(".v"):
                out.append(os.path.join(root, fn))
    out.sort()
    return out


def main() -> int:
    # Make stdout robust on Windows consoles (avoid crash on Vietnamese paths).
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")  # type: ignore[attr-defined]
    except Exception:
        pass

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    examples_dir = os.path.join(repo_root, "examples")

    if not os.path.isdir(examples_dir):
        print(f"[ERROR] examples dir not found: {examples_dir}")
        return 2

    # Import here so running this tool doesn't require MyLogic to be installed as a package.
    sys.path.insert(0, repo_root)
    from core.export import netlist_to_verilog
    from core.synthesis.aig import aig_to_netlist
    from core.synthesis.synthesis_flow import synthesize
    from frontends.verilog import parse_verilog, parse_verilog_ast

    use_ast = os.environ.get("MYLOGIC_USE_AST", "").strip() not in ("", "0", "false", "False")

    results: List[CheckResult] = []
    files = _walk_verilog_files(examples_dir)
    if not files:
        print("[WARN] No .v files found under examples/")
        return 0

    for path in files:
        expected_ok = not _is_expected_fail(path)
        try:
            nl = (parse_verilog_ast(path) if use_ast else parse_verilog(path, strict=True))
        except Exception as e:  # ParserError or others
            ok = False
            results.append(CheckResult(path, ok, expected_ok, "parse", str(e)))
            continue

        try:
            aig = synthesize(nl)
        except Exception as e:
            ok = False
            results.append(CheckResult(path, ok, expected_ok, "synthesize", str(e)))
            continue

        try:
            snl = aig_to_netlist(aig, nl)
            _ = netlist_to_verilog(snl, module_name=snl.get("name"))
        except Exception as e:
            ok = False
            results.append(CheckResult(path, ok, expected_ok, "export_verilog", str(e)))
            continue

        results.append(CheckResult(path, True, expected_ok, "ok", None))

    # Treat "expected OK but failed" as errors; "expected FAIL but passed" as warnings.
    unexpected_failures: List[CheckResult] = [r for r in results if (r.expected_ok and not r.ok)]
    unexpected_passes: List[CheckResult] = [r for r in results if ((not r.expected_ok) and r.ok)]
    expected_fails = [r for r in results if (not r.ok) and (not r.expected_ok)]
    expected_oks = [r for r in results if r.ok and r.expected_ok]

    print(f"[INFO] MYLOGIC_USE_AST={use_ast}")
    print(f"[INFO] Total files: {len(results)}")
    print(f"[INFO] Expected OK and OK: {len(expected_oks)}")
    print(f"[INFO] Expected FAIL and FAIL: {len(expected_fails)}")
    print(f"[INFO] Unexpected failures: {len(unexpected_failures)}")
    print(f"[INFO] Unexpected passes (warning): {len(unexpected_passes)}")

    if unexpected_failures:
        print("\n[UNEXPECTED FAILURES]")
        for r in unexpected_failures:
            rel = os.path.relpath(r.path, repo_root).replace("\\", "/")
            exp = "OK" if r.expected_ok else "FAIL"
            got = "OK" if r.ok else "FAIL"
            print(f"- {rel}: expected {exp}, got {got} at {r.stage}")
            if r.error:
                msg = r.error.replace("\n", " ").strip()
                if len(msg) > 300:
                    msg = msg[:300] + "..."
                try:
                    print(f"    {msg}")
                except UnicodeEncodeError:
                    safe = msg.encode("utf-8", "backslashreplace").decode("utf-8")
                    print(f"    {safe}")

    if unexpected_passes:
        print("\n[UNEXPECTED PASSES (warnings)]")
        for r in unexpected_passes:
            rel = os.path.relpath(r.path, repo_root).replace("\\", "/")
            print(f"- {rel}")

    return 1 if unexpected_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

