module complex_arithmetic(a, b, c, d, result1, result2, result3);
  input [3:0] a, b, c, d;
  output [4:0] result1;
  output [7:0] result2;
  output [3:0] result3;
  
  // Complex arithmetic expressions
  assign result1 = (a + b) - (c - d);
  assign result2 = (a * b) + (c * d);
  assign result3 = (a / b) + (c % d);
endmodule
