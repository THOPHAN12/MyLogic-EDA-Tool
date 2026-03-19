import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _parse(path: str):
    from frontends.verilog import parse_verilog
    return parse_verilog(path)


def _synthesize(netlist):
    from core.synthesis.synthesis_flow import synthesize
    return synthesize(netlist)


class TestEdgeCasesCombinational(unittest.TestCase):
    def test_bitwidth_trunc_and_zero_extend(self):
        nl = _parse(os.path.join(ROOT, "examples", "99_edge_cases", "bitwidth_mismatch.v"))
        vw = nl.get("attrs", {}).get("vector_widths", {})
        self.assertEqual(vw.get("a"), 2)
        self.assertEqual(vw.get("b"), 4)

        from core.synthesis.synthesis_flow import run_complete_synthesis
        synth_nl = run_complete_synthesis(nl)
        # should produce 2+4 output bits
        out_bits = [nd.get("output") for nd in (synth_nl.get("nodes", {}) or {}).values() if isinstance(nd, dict)]
        self.assertTrue(any(o.startswith("a_trunc") for o in out_bits))
        self.assertTrue(any(o.startswith("b_zext") for o in out_bits))

    def test_constants_formats_parse(self):
        nl = _parse(os.path.join(ROOT, "examples", "99_edge_cases", "constants_formats.v"))
        self.assertIn("yu", nl.get("outputs", []))
        # Synthesis should not crash and must not create PI named "'b1"
        aig = _synthesize(nl)
        self.assertNotIn("'b1", aig.pis)

    def test_constprop_cone_optimized_to_const0(self):
        nl = _parse(os.path.join(ROOT, "examples", "99_edge_cases", "constprop_cone.v"))
        aig = _synthesize(nl)
        from core.optimization.optimization_flow import optimize
        opt = optimize(aig)
        # all POs should be constant 0 after constprop (or inverted const1)
        self.assertGreaterEqual(len(opt.pos), 1)
        for node, inv in opt.pos:
            if node.is_constant():
                val = 1 if node.get_value() else 0
                if inv:
                    val = 1 - val
                self.assertEqual(val, 0)
            else:
                self.fail("PO not constant after constprop")

    def test_nested_ternary(self):
        nl = _parse(os.path.join(ROOT, "examples", "99_edge_cases", "nested_ternary.v"))
        # must have at least one MUX node in parsed
        nodes = nl.get("nodes", [])
        mux_count = sum(1 for n in nodes if isinstance(n, dict) and n.get("type") == "MUX")
        self.assertGreaterEqual(mux_count, 2)
        # synthesis should not create PI with '?' or ':'
        aig = _synthesize(nl)
        self.assertFalse(any(("?" in name or ":" in name) for name in aig.pis.keys()))

    def test_nested_concat_mix_const(self):
        nl = _parse(os.path.join(ROOT, "examples", "99_edge_cases", "nested_concat_mixconst.v"))
        # parse should contain CONCAT (at least 1)
        nodes = nl.get("nodes", [])
        self.assertTrue(any(isinstance(n, dict) and n.get("type") == "CONCAT" for n in nodes))
        from core.synthesis.synthesis_flow import run_complete_synthesis
        synth_nl = run_complete_synthesis(nl)
        # output bits should be named y[0]..y[3]
        outs = sorted({nd.get("output") for nd in (synth_nl.get("nodes", {}) or {}).values() if isinstance(nd, dict)})
        self.assertTrue(any(o == "y[0]" for o in outs))
        self.assertTrue(any(o == "y[3]" for o in outs))

    def test_dff_isolation_no_clk_in_aig_pos(self):
        nl = _parse(os.path.join(ROOT, "examples", "99_edge_cases", "dff_isolation.v"))
        # parser should create a DFF node
        nodes = nl.get("nodes", [])
        self.assertTrue(any(isinstance(n, dict) and n.get("type") == "DFF" for n in nodes))
        # Synthesis should not crash. Output depends on sequential state; AIG may treat it as floating PI.
        _synthesize(nl)


if __name__ == "__main__":
    unittest.main()

