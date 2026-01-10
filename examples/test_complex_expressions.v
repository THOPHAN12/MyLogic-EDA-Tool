/*
 * Test Complex Expressions with NOT
 * 
 * Test các expressions phức tạp:
 * - (a | b) | c - Nested OR
 * - ~(a & b) | (c ^ d) - NOT AND combined with XOR
 * - (a & b) ^ ~c - AND XOR NOT
 * - ~(a | (b & c)) - NOT OR AND nested
 */

module test_complex_expressions(
    input a,
    input b,
    input c,
    input d,
    output nested_or,              // (a | b) | c
    output not_and_or_xor,         // ~(a & b) | (c ^ d)
    output and_xor_not,            // (a & b) ^ ~c
    output not_or_and_nested       // ~(a | (b & c))
);

    assign nested_or = (a | b) | c;
    assign not_and_or_xor = ~(a & b) | (c ^ d);
    assign and_xor_not = (a & b) ^ ~c;
    assign not_or_and_nested = ~(a | (b & c));
    
endmodule


