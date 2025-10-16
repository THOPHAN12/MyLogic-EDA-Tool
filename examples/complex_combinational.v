/*
 * Complex Combinational Circuit Example
 * MyLogic EDA Tool - Advanced Combinational Logic
 * 
 * Ví dụ về mạch tổ hợp phức tạp với nhiều operations
 */

module complex_combinational(
    input [3:0] a, b, c, d,      // 4-bit inputs
    input [1:0] sel,             // 2-bit selector
    output [4:0] result1,         // 5-bit output
    output [7:0] result2,         // 8-bit output
    output [3:0] result3,        // 4-bit output
    output [1:0] flags            // 2-bit flags
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

/*
 * Advanced Arithmetic Unit
 */
module arithmetic_unit(
    input [3:0] x, y,             // Operands
    input [2:0] op,               // Operation code
    output [7:0] result,          // Result
    output overflow,              // Overflow flag
    output zero                   // Zero flag
);

// Operation decoding
wire add_op = (op == 3'b000);
wire sub_op = (op == 3'b001);
wire mul_op = (op == 3'b010);
wire div_op = (op == 3'b011);
wire and_op = (op == 3'b100);
wire or_op  = (op == 3'b101);
wire xor_op = (op == 3'b110);
wire not_op = (op == 3'b111);

// Arithmetic operations
wire [4:0] sum = x + y;
wire [4:0] diff = x - y;
wire [7:0] product = x * y;
wire [3:0] quotient = x / y;

// Bitwise operations
wire [3:0] and_result = x & y;
wire [3:0] or_result = x | y;
wire [3:0] xor_result = x ^ y;
wire [3:0] not_result = ~x;

// Result selection
assign result = add_op ? {3'b000, sum} :
                sub_op ? {3'b000, diff} :
                mul_op ? product :
                div_op ? {4'b0000, quotient} :
                and_op ? {4'b0000, and_result} :
                or_op  ? {4'b0000, or_result} :
                xor_op ? {4'b0000, xor_result} :
                {4'b0000, not_result};

// Flag generation
assign overflow = (add_op && (sum[4] != sum[3])) ||
                 (sub_op && (diff[4] != diff[3]));

assign zero = (result == 8'b00000000) ? 1'b1 : 1'b0;

endmodule

/*
 * Priority Encoder
 */
module priority_encoder(
    input [7:0] in,               // 8-bit input
    output [2:0] out,             // 3-bit output
    output valid                  // Valid signal
);

// Priority encoding logic
assign out = (in[7]) ? 3'b111 :
             (in[6]) ? 3'b110 :
             (in[5]) ? 3'b101 :
             (in[4]) ? 3'b100 :
             (in[3]) ? 3'b011 :
             (in[2]) ? 3'b010 :
             (in[1]) ? 3'b001 :
             3'b000;

assign valid = (in != 8'b00000000) ? 1'b1 : 1'b0;

endmodule
