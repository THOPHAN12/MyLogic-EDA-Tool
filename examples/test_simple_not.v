/*
 * Test Simple NOT Operations
 * 
 * Test các trường hợp NOT đơn giản:
 * - ~a - Simple NOT
 * - ~b - Simple NOT
 * - Multiple simple NOTs
 */

module test_simple_not(
    input a,
    input b,
    output not_a,
    output not_b
);

    assign not_a = ~a;
    assign not_b = ~b;
    
endmodule


