import os
import tempfile
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestVerilogExport(unittest.TestCase):
    def test_export_synthesized_verilog_contains_module(self):
        from frontends.verilog import parse_verilog
        from core.synthesis.synthesis_flow import run_complete_synthesis
        from core.export import netlist_to_verilog

        path = os.path.join(ROOT, "examples", "02_always_blocks", "test_always_combinational.v")
        # file may be edited by user; use loose to avoid syntax-typo rules in this test suite
        nl = parse_verilog(path, strict=False)
        synth_nl = run_complete_synthesis(nl)
        v = netlist_to_verilog(synth_nl, module_name="test_always_combinational_synth")
        self.assertIn("module test_always_combinational_synth", v)
        self.assertIn("endmodule", v)
        self.assertIn("assign", v)


if __name__ == "__main__":
    unittest.main()

