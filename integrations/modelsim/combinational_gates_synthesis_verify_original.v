module combinational_gates_synthesis_verify_original(
  input a, b, c,
  output out_and, out_or, out_xor, out_nand, out_nor, out_not
);

  // Internal wires
  wire _temp_3;
  wire _temp_5;
  wire and_0;
  wire and_3;
  wire not_4;
  wire not_6;
  wire not_7;
  wire or_1;
  wire or_5;
  wire xor_2;

  // Logic implementation
  assign _temp_3 = a & b;
  assign _temp_5 = a | b;
  assign and_0 = a & b;
  assign or_1 = a | b | c;
  assign xor_2 = a ^ b;
  assign and_3 = a & b;
  assign not_4 = ~_temp_3;
  assign or_5 = a | b;
  assign not_6 = ~_temp_5;
  assign not_7 = ~a;

endmodule