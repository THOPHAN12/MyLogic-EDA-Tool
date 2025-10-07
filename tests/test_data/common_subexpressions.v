/*
 * Common subexpressions test case for CSE algorithm
 * Contains repeated subexpressions that should be shared
 */

module common_subexpressions (
    input a,
    input b,
    input c,
    input d,
    output out1,
    output out2
);

// Common subexpression: a & b appears multiple times
assign temp1 = a & b;
assign temp2 = a & b;  // Same as temp1
assign temp3 = a & b;  // Same as temp1

assign out1 = temp1 | c;
assign out2 = temp2 & temp3;

endmodule
