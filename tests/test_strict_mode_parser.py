import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestStrictModeParser(unittest.TestCase):
    def test_implicit_wire_raises(self):
        from frontends.verilog.core.parser import parse_verilog
        from core.utils.error_handling import ParserError

        path = os.path.join(ROOT, "examples", "99_edge_cases", "implicit_wire_should_fail.v")
        with self.assertRaises(ParserError):
            parse_verilog(path, strict=True)

    def test_default_nettype_none_raises(self):
        from frontends.verilog.core.parser import parse_verilog
        from core.utils.error_handling import ParserError
        import os

        path = os.path.join(ROOT, "examples", "99_edge_cases", "default_nettype_none_should_fail.v")
        with self.assertRaises(ParserError):
            parse_verilog(path, strict=False)


if __name__ == "__main__":
    unittest.main()

