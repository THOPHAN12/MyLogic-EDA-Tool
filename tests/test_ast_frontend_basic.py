import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestAstFrontendBasic(unittest.TestCase):
    def test_ast_parse_rejects_forbidden(self):
        from frontends.verilog.ast.ast_parser import parse_myverilog_ast
        bad = "module m(input wire a, output wire y); initial y = 0; endmodule"
        with self.assertRaises(Exception):
            parse_myverilog_ast(bad, "<mem>")

    def test_ast_frontend_parses_assign(self):
        from frontends.verilog.ast.netlist_gen import parse_verilog_ast
        import tempfile

        try:
            import lark  # noqa: F401
        except Exception:
            self.skipTest("lark not installed in current environment")

        src = """
        module m(input wire a, input wire b, output wire y);
          assign y = a & b;
        endmodule
        """
        with tempfile.NamedTemporaryFile("w", suffix=".v", delete=False, encoding="utf-8") as f:
            f.write(src)
            p = f.name

        nl = parse_verilog_ast(p, strict=True)
        self.assertEqual(nl["name"], "m")
        self.assertIn("a", nl["inputs"])
        self.assertIn("y", nl["outputs"])
        self.assertTrue(any(n.get("type") == "AND" for n in nl.get("nodes", [])))


if __name__ == "__main__":
    unittest.main()

