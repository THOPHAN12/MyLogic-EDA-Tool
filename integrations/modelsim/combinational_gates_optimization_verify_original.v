module combinational_gates_optimization_verify_original(
  input a, b, c,
  output out_and, out_or, out_xor, out_nand, out_nor, out_not
);

  // Internal wires
  wire not_a;
  wire not_b;
  wire not_c;
  wire not_w10;
  wire not_w12;
  wire not_w13;
  wire not_w16;
  wire not_w19;
  wire not_w5;
  wire not_w9;
  wire w10;
  wire w12;
  wire w13;
  wire w14;
  wire w15;
  wire w16;
  wire w19;
  wire w5;
  wire w6;
  wire w7;
  wire w8;
  wire w9;

  // Logic implementation
  assign out_and = a & b;
  assign not_c = ~c;
  assign w8 = not_c & 1'b1;
  assign not_a = ~a;
  assign w6 = not_a & 1'b1;
  assign not_b = ~b;
  assign w7 = not_b & 1'b1;
  assign w9 = w6 & w7;
  assign w10 = w8 & w9;
  assign not_w10 = ~w10;
  assign out_or = not_w10 & 1'b1;
  assign w12 = b & w6;
  assign not_w12 = ~w12;
  assign w14 = not_w12 & 1'b1;
  assign w13 = a & w7;
  assign not_w13 = ~w13;
  assign w15 = not_w13 & 1'b1;
  assign w16 = w14 & w15;
  assign not_w16 = ~w16;
  assign out_xor = not_w16 & 1'b1;
  assign not_w5 = ~w5;
  assign out_nand = not_w5 & 1'b1;
  assign not_w9 = ~w9;
  assign w19 = not_w9 & 1'b1;
  assign not_w19 = ~w19;
  assign out_nor = not_w19 & 1'b1;

endmodule