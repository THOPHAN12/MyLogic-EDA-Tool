module simple_multiplier(a, b, product);
  input [3:0] a, b;
  output [7:0] product;
  
  assign product = a * b;
endmodule
