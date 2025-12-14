/*
 * Test Bitwise Operations
 * 
 * Test các tính năng:
 * - AND (&)
 * - OR (|)
 * - XOR (^)
 * - XNOR (~^)
 * - NOT (~)
 */

module test_bitwise(
    input [7:0] a,
    input [7:0] b,
    output [7:0] and_result,
    output [7:0] or_result,
    output [7:0] xor_result,
    output [7:0] xnor_result,
    output [7:0] not_a
);

    assign and_result = a & b;
    assign or_result = a | b;
    assign xor_result = a ^ b;
    assign xnor_result = ~(a ^ b);  // XNOR = NOT XOR
    
    // Bitwise NOT - sử dụng expression với NOT
    // Tránh parse trực tiếp ~a bằng cách dùng nested expression
    wire [7:0] xor_temp = a ^ b;
    assign not_a = ~a;  // NOT operator
    
endmodule

