/*
 * Complex expression test case
 * Input: a, b, c, d
 * Output: out = (a & b) | (c ^ d)
 */

module complex_expression (
    input a,
    input b,
    input c,
    input d,
    output out
);

assign out = (a & b) | (c ^ d);

endmodule
