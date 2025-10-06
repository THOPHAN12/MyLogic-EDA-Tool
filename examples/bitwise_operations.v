module bitwise_operations(a, b, and_out, or_out, xor_out, not_out);
  input [3:0] a, b;
  output [3:0] and_out, or_out, xor_out, not_out;
  
  assign and_out = a & b;      // Bitwise AND
  assign or_out = a | b;      // Bitwise OR
  assign xor_out = a ^ b;     // Bitwise XOR
  assign not_out = ~a;        // Bitwise NOT
endmodule
