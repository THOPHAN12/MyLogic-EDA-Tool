import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestSyntaxErrorCatchall(unittest.TestCase):
    def _p(self, name: str):
        from frontends.verilog import parse_verilog
        path = os.path.join(ROOT, "examples", "99_edge_cases", "syntax_errors", name)
        with self.assertRaises(Exception):
            parse_verilog(path)

    def test_double_semicolon(self):
        self._p("double_semicolon.v")

    def test_unbalanced_paren(self):
        self._p("unbalanced_paren.v")

    def test_begin_end_mismatch(self):
        self._p("begin_end_mismatch.v")

    def test_trailing_comma_portlist(self):
        self._p("trailing_comma_portlist.v")

    def test_end_semicolon(self):
        self._p("end_semicolon.v")


if __name__ == "__main__":
    unittest.main()

