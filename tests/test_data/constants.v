/*
 * Constants test case for ConstProp algorithm
 * Contains constant values that should be propagated
 */

module constants (
    input a,
    input b,
    output out1,
    output out2,
    output out3
);

// Constant propagation
assign const_zero = 1'b0;
assign const_one = 1'b1;

// Logic with constants
assign out1 = a & const_one;  // Should become: out1 = a
assign out2 = b | const_zero;  // Should become: out2 = b
assign out3 = a & const_zero;  // Should become: out3 = 1'b0

endmodule
