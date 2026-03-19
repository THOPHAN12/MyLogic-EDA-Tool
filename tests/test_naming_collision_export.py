import unittest


class TestNamingCollisionExport(unittest.TestCase):
    def test_internal_names_use_reserved_prefix(self):
        # User intentionally uses names that would collide with old exporter: w0, not_w0, n0, temp_out0
        verilog = r"""
        module collide(
          input wire a,
          input wire b,
          output wire w0,
          output wire not_w0,
          output wire n0,
          output wire temp_out0
        );
          assign w0 = a & b;
          assign not_w0 = ~w0;
          assign n0 = w0 | a;
          assign temp_out0 = n0 ^ b;
        endmodule
        """

        from frontends.verilog import parse_verilog
        from core.synthesis.synthesis_flow import synthesize
        from core.synthesis.aig import aig_to_netlist

        # write a temp file (no in-memory parser helper in this project)
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".v", delete=False, encoding="utf-8") as f:
            f.write(verilog)
            tmp_path = f.name
        nl = parse_verilog(tmp_path)
        aig = synthesize(nl)
        out_nl = aig_to_netlist(aig, nl)

        # Exported internal nets/node IDs should start with __ml_ (reserved prefix)
        nodes = out_nl.get("nodes", {}) or {}
        internal_ids = [nid for nid in nodes.keys() if nid.startswith("__ml_")]
        self.assertTrue(internal_ids, "expected internal node ids with reserved prefix")

        # No exported node id should equal user signal names
        user_names = {"w0", "not_w0", "n0", "temp_out0"}
        self.assertTrue(user_names.issubset(set(nl.get("outputs", []))))
        for nid in nodes.keys():
            self.assertNotIn(nid, user_names)

        # Any internal generated output wires should use the reserved prefix too
        outputs = [nd.get("output") for nd in nodes.values() if isinstance(nd, dict)]
        for o in outputs:
            if o and (o.startswith("w") or o.startswith("not_") or o.startswith("temp_out")):
                # these are internal patterns in the exporter; they should now be prefixed
                self.assertTrue(o.startswith("__ml_") or o in user_names or o.startswith("out") or o.startswith("result") or "[" in o)


if __name__ == "__main__":
    unittest.main()

