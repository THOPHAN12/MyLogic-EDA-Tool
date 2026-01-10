module test_arithmetic_synthesis_verify_original(
  input a, b,
  output sum, diff, prod, quot, mod
);

  // Internal wires
  wire add_0;
  wire div_3;
  wire mod_4;
  wire mul_2;
  wire sub_1;

  // Logic implementation
  assign add_0 = a & b;
  assign sub_1 = a & b;
  assign mul_2 = a & b;
  assign div_3 = a & b;
  assign mod_4 = a & b;

endmodule