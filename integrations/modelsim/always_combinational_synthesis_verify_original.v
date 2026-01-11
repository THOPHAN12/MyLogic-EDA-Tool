module always_combinational_synthesis_verify_original(
  input a, b, c,
  output out1, out2
);

  // Internal wires
  wire _temp_1;
  wire and_0;
  wire and_2;
  wire or_1;

  // Logic implementation
  assign _temp_1 = a | b;
  assign and_0 = a & b;
  assign or_1 = a | b;
  assign and_2 = and_0 & c;

endmodule