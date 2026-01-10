/*
 * Test Nested NOT Operations
 * 
 * Test các trường hợp NOT với nested expressions:
 * - ~(a & b) - NOT AND
 * - ~(a | b) - NOT OR
 * - ~(a ^ b) - NOT XOR (XNOR)
 * - ~((a & b) | c) - Double nested
 * - ~(a & (b | c)) - Multiple nested
 */

module test_nested_not(
    input a,
    input b,
    input c,
    output not_and_result,     // ~(a & b)
    output not_or_result,       // ~(a | b)
    output not_xor_result,      // ~(a ^ b)
    output double_nested,       // ~((a & b) | c)
    output multiple_nested      // ~(a & (b | c))
);

    assign not_and_result = ~(a & b);
    assign not_or_result = ~(a | b);
    assign not_xor_result = ~(a ^ b);
    assign double_nested = ~((a & b) | c);
    assign multiple_nested = ~(a & (b | c));
    
endmodule


