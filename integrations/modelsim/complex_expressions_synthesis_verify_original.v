module complex_expressions_synthesis_verify_original(
  input a, b, c, d,
  output out1, out2, out3
);

  // Internal wires
  wire _temp_0;
  wire _temp_1;
  wire _temp_3;
  wire _temp_5;
  wire and_0;
  wire and_1;
  wire and_3;
  wire and_5;
  wire not_6;
  wire or_2;
  wire or_4;

  // Logic implementation
  assign _temp_0 = a & b;
  assign _temp_1 = c & d;
  assign _temp_3 = a & b & c;
  assign _temp_5 = a & b;
  assign and_0 = a & b;
  assign and_1 = c & d;
  assign or_2 = _temp_0 | and_0;
  assign and_3 = a & b & c;
  assign or_4 = or_2 | d;
  assign and_5 = a & b;
  assign not_6 = ~_temp_5;

endmodule