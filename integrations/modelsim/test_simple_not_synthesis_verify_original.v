module test_simple_not_synthesis_verify_original(
  input a, b,
  output not_a, not_b
);

  // Internal wires
  wire not_0;
  wire not_1;

  // Logic implementation
  assign not_0 = ~a;
  assign not_1 = ~b;

endmodule