module dead_code_test(a, b, c, result);
  input [3:0] a, b, c;
  output [4:0] result;
  
  // This will be used
  assign result = a + b;
  
  // This is dead code (unused)
  wire [3:0] unused_sum = a + c;
  wire [3:0] unused_diff = a - c;
  wire [3:0] unused_prod = a * c;
  
  // More dead code
  wire [3:0] dead_wire1 = b + c;
  wire [3:0] dead_wire2 = b - c;
endmodule
