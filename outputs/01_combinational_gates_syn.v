module combinational_gates_syn(
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
  wire __ml_w14;
  wire __ml_w15;
  wire __ml_w16;
  wire __ml_w17;
  wire __ml_w18;
  wire __ml_w19;
  wire __ml_w20;
  wire __ml_w24;
  wire __ml_w25;
  wire __ml_w26;
  wire __ml_w27;
  wire __ml_w28;
  wire __ml_w6;
  wire __ml_w7;
  wire __ml_w8;
  wire __ml_w9;

  assign out_and = a & b;
  assign __ml_w9 = ~d;
  assign __ml_w8 = ~c;
  assign __ml_w6 = ~a;
  assign __ml_w7 = ~b;
  assign __ml_w10 = __ml_w6 & __ml_w7;
  assign __ml_w11 = __ml_w8 & __ml_w10;
  assign __ml_w12 = __ml_w9 & __ml_w11;
  assign out_or = ~__ml_w12;
  assign __ml_w14 = ~a;
  assign __ml_w16 = b & __ml_w14;
  assign __ml_w18 = ~__ml_w16;
  assign __ml_w15 = ~b;
  assign __ml_w17 = a & __ml_w15;
  assign __ml_w19 = ~__ml_w17;
  assign __ml_w20 = __ml_w18 & __ml_w19;
  assign out_xor = ~__ml_w20;
  assign __ml_w24 = a & b;
  assign out_nand = ~__ml_w24;
  assign __ml_w25 = ~a;
  assign __ml_w26 = ~b;
  assign __ml_w27 = __ml_w25 & __ml_w26;
  assign __ml_w28 = ~__ml_w27;
  assign out_nor = ~__ml_w28;
  assign out_not = ~a;
endmodule
