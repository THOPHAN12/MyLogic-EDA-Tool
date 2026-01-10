module test_bitwise_synthesis_verify_original(
  input a, b,
  output and_result, or_result, xor_result, xnor_result, not_a
);

  // Internal wires
  wire and_0;
  wire not_3;
  wire not_4;
  wire or_1;
  wire xor_2;

  // Logic implementation
  assign and_0 = a & b;
  assign or_1 = a | b;
  assign xor_2 = a ^ b;
  assign not_3 = ~(a ^ b);
  assign not_4 = ~a;

endmodule