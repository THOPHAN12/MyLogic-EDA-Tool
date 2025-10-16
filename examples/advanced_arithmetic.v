/*
 * Advanced Arithmetic Unit - Combinational Logic
 * MyLogic EDA Tool - Complex Combinational Circuit
 */

module advanced_arithmetic(
    input [3:0] a, b, c, d,      // 4-bit inputs
    input [1:0] sel,             // 2-bit selector
    output [4:0] result1,       // 5-bit output
    output [7:0] result2,       // 8-bit output
    output [3:0] result3,       // 4-bit output
    output [1:0] flags           // 2-bit flags
);

// Complex arithmetic operations
wire [4:0] sum_ab = a + b;
wire [4:0] diff_cd = c - d;
wire [7:0] prod_ab = a * b;
wire [3:0] quot_cd = c / d;

// Multiplexer logic
assign result1 = (sel == 2'b00) ? sum_ab :
                 (sel == 2'b01) ? diff_cd :
                 (sel == 2'b10) ? {1'b0, a} :
                 {1'b0, b};

// Complex expression với parentheses
assign result2 = (a * b) + (c * d) + (a & b);

// Bitwise operations
assign result3 = (a & b) | (c ^ d);

// Flag generation
assign flags[0] = (a > b) ? 1'b1 : 1'b0;  // Greater than
assign flags[1] = (c == d) ? 1'b1 : 1'b0;  // Equal

endmodule
