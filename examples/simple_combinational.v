module simple_combinational(a, b, c, d, sel, result1, result2, result3, flags);
  input [3:0] a, b, c, d;
  input [1:0] sel;
  output [4:0] result1;
  output [7:0] result2;
  output [3:0] result3;
  output [1:0] flags;
  
  assign result1 = (sel == 2'b00) ? (a + b) : (c - d);
  assign result2 = (a * b) + (c * d);
  assign result3 = (a & b) | (c ^ d);
  assign flags[0] = (a > b) ? 1'b1 : 1'b0;
  assign flags[1] = (c == d) ? 1'b1 : 1'b0;
endmodule
