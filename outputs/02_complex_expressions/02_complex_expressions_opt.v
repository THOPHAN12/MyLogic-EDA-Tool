module complex_expressions_opt(
  input  wire a,
  input  wire b,
  input  wire c,
  input  wire d,
  output wire out1,
  output wire out2,
  output wire out3
);

  wire __ml_w10;
  wire __ml_w12;
  wire __ml_w13;
  wire __ml_w14;
  wire __ml_w15;
  wire __ml_w6;
  wire __ml_w7;
  wire __ml_w8;
  wire __ml_w9;

  assign __ml_w6 = a & b;
  assign __ml_w7 = ~__ml_w6;
  assign __ml_w8 = c & d;
  assign __ml_w9 = ~__ml_w8;
  assign __ml_w10 = __ml_w7 & __ml_w9;
  assign out1 = ~__ml_w10;
  assign __ml_w12 = c & __ml_w6;
  assign __ml_w13 = ~__ml_w12;
  assign __ml_w14 = ~d;
  assign __ml_w15 = __ml_w13 & __ml_w14;
  assign out2 = ~__ml_w15;
  assign out3 = __ml_w7;
endmodule
