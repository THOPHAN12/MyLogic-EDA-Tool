module test_arithmetic_optimization_verify_original(
  input a, b,
  output sum, diff, prod, quot, mod
);

  // Internal wires
  wire not_a[0];
  wire not_b[0];
  wire not_w188;
  wire not_w189;
  wire not_w192;
  wire not_w193;
  wire not_w194;
  wire not_w195;
  wire not_w21;
  wire not_w22;
  wire not_w23;
  wire not_w26;
  wire not_w27;
  wire not_w28;
  wire w187;
  wire w188;
  wire w189;
  wire w190;
  wire w191;
  wire w192;
  wire w193;
  wire w194;
  wire w195;
  wire w20;
  wire w21;
  wire w22;
  wire w23;
  wire w24;
  wire w25;
  wire w26;
  wire w27;
  wire w28;

  // Logic implementation
  assign not_a[0] = ~a[0];
  assign w20 = not_a[0] & 1'b1;
  assign w22 = b[0] & w20;
  assign not_w22 = ~w22;
  assign w24 = not_w22 & 1'b1;
  assign not_b[0] = ~b[0];
  assign w21 = not_b[0] & 1'b1;
  assign w23 = a[0] & w21;
  assign not_w23 = ~w23;
  assign w25 = not_w23 & 1'b1;
  assign w26 = w24 & w25;
  assign not_w26 = ~w26;
  assign w27 = not_w26 & 1'b1;
  assign not_w27 = ~w27;
  assign w28 = not_w27 & 1'b1;
  assign not_w28 = ~w28;
  assign sum = not_w28 & 1'b1;
  assign w188 = w20 & w21;
  assign not_w188 = ~w188;
  assign w190 = not_w188 & 1'b1;
  assign not_w21 = ~w21;
  assign w187 = not_w21 & 1'b1;
  assign w189 = a[0] & w187;
  assign not_w189 = ~w189;
  assign w191 = not_w189 & 1'b1;
  assign w192 = w190 & w191;
  assign not_w192 = ~w192;
  assign w193 = not_w192 & 1'b1;
  assign not_w193 = ~w193;
  assign w194 = not_w193 & 1'b1;
  assign not_w194 = ~w194;
  assign w195 = not_w194 & 1'b1;
  assign not_w195 = ~w195;
  assign diff = not_w195 & 1'b1;

endmodule