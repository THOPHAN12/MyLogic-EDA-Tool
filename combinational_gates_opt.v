module combinational_gates_opt(
  input  wire a,
  input  wire b,
  input  wire c,
  input  wire d,
  output wire out_and,
  output wire out_or,
  output wire out_xor,
  output wire out_nand,
  output wire out_nor,
  output wire out_not
);

  wire __ml_w10;
  wire __ml_w11;
  wire __ml_w12;
  wire __ml_w13;
  wire __ml_w15;
  wire __ml_w16;
  wire __ml_w17;
  wire __ml_w18;
  wire __ml_w19;
  wire __ml_w22;
  wire __ml_w7;
  wire __ml_w8;
  wire __ml_w9;

  assign out_and = a & b;
  assign __ml_w7 = ~d;
  assign __ml_w8 = ~c;
  assign __ml_w9 = ~a;
  assign __ml_w10 = ~b;
  assign __ml_w11 = __ml_w9 & __ml_w10;
  assign __ml_w12 = __ml_w8 & __ml_w11;
  assign __ml_w13 = __ml_w7 & __ml_w12;
  assign out_or = ~__ml_w13;
  assign __ml_w15 = b & __ml_w9;
  assign __ml_w16 = ~__ml_w15;
  assign __ml_w17 = a & __ml_w10;
  assign __ml_w18 = ~__ml_w17;
  assign __ml_w19 = __ml_w16 & __ml_w18;
  assign out_xor = ~__ml_w19;
  assign out_nand = ~out_and;
  assign __ml_w22 = ~__ml_w11;
  assign out_nor = ~__ml_w22;
  assign out_not = __ml_w9;
endmodule
