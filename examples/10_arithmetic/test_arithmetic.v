/*
 * Test Arithmetic Operations
 * 
 * Test các tính năng:
 * - Addition (+)
 * - Subtraction (-)
 * - Multiplication (*)
 * - Division (/)
 * - Modulo (%)
 */

module test_arithmetic(
    input [7:0] a,
    input [7:0] b,
    output [8:0] sum,
    output [8:0] diff,
    output [15:0] prod,
    output [7:0] quot,
    output [7:0] mod
);

    assign sum = a + b;
    assign diff = a - b;
    assign prod = a * b;
    assign quot = a / b;
    assign mod = a % b;
    
endmodule

