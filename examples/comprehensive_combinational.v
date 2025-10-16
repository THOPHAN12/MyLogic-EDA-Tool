/*
 * Comprehensive Combinational Verilog Syntax Examples
 * MyLogic EDA Tool - Complete Syntax Support
 * 
 * Tổng hợp tất cả syntax Verilog cho mạch tổ hợp
 */

// ============================================================================
// 1. MODULE DECLARATIONS
// ============================================================================

// Port list style (recommended)
module comprehensive_combinational(
    // Vector inputs
    input [3:0] a, b, c, d,           // 4-bit inputs
    input [1:0] sel,                  // 2-bit selector
    input [7:0] data_in,              // 8-bit data input
    
    // Scalar inputs
    input enable,                     // 1-bit enable
    input clk_en,                     // 1-bit clock enable
    
    // Vector outputs
    output [4:0] result1,             // 5-bit result
    output [7:0] result2,             // 8-bit result
    output [3:0] result3,             // 4-bit result
    
    // Scalar outputs
    output valid,                     // 1-bit valid flag
    output overflow                   // 1-bit overflow flag
);

// ============================================================================
// 2. WIRE DECLARATIONS
// ============================================================================

// Vector wires
wire [4:0] sum_ab = a + b;           // 5-bit sum
wire [4:0] diff_cd = c - d;          // 5-bit difference
wire [7:0] prod_ab = a * b;          // 8-bit product
wire [3:0] quot_cd = c / d;          // 4-bit quotient

// Scalar wires
wire and_result = a[0] & b[0];       // 1-bit AND
wire or_result = a[1] | b[1];        // 1-bit OR
wire xor_result = a[2] ^ b[2];       // 1-bit XOR
wire not_result = ~a[3];             // 1-bit NOT

// ============================================================================
// 3. ARITHMETIC OPERATIONS
// ============================================================================

// Addition
assign result1 = a + b;              // Simple addition
assign result2 = (a + b) + (c + d);  // Complex addition with parentheses

// Subtraction
assign result3 = a - b;              // Simple subtraction

// Multiplication
wire [7:0] mult_result = a * b;      // Multiplication

// Division
wire [3:0] div_result = a / b;       // Division

// ============================================================================
// 4. BITWISE OPERATIONS
// ============================================================================

// AND operations
wire [3:0] and_vec = a & b;          // Vector AND
wire and_scalar = a[0] & b[0];       // Scalar AND

// OR operations
wire [3:0] or_vec = a | b;           // Vector OR
wire or_scalar = a[1] | b[1];        // Scalar OR

// XOR operations
wire [3:0] xor_vec = a ^ b;          // Vector XOR
wire xor_scalar = a[2] ^ b[2];       // Scalar XOR

// NOT operations
wire [3:0] not_vec = ~a;             // Vector NOT
wire not_scalar = ~a[3];             // Scalar NOT

// ============================================================================
// 5. TERNARY OPERATORS (CONDITIONAL ASSIGNMENTS)
// ============================================================================

// Simple ternary
assign valid = (a > b) ? 1'b1 : 1'b0;

// Nested ternary
assign overflow = (a + b > 4'b1111) ? 1'b1 : 
                  (a + b < 4'b0000) ? 1'b1 : 1'b0;

// Complex ternary with expressions
assign result1 = (sel == 2'b00) ? (a + b) :
                 (sel == 2'b01) ? (a - b) :
                 (sel == 2'b10) ? (a * b) :
                 (a / b);

// ============================================================================
// 6. COMPLEX EXPRESSIONS WITH PARENTHESES
// ============================================================================

// Arithmetic with parentheses
assign result2 = ((a + b) * (c - d)) + ((a * b) / (c + d));

// Bitwise with parentheses
assign result3 = ((a & b) | (c ^ d)) & ((~a) | (~b));

// Mixed operations
wire [4:0] complex_expr = ((a + b) & (c - d)) | ((a * b) ^ (c / d));

// ============================================================================
// 7. BIT SELECTIONS AND CONCATENATIONS
// ============================================================================

// Bit selections
assign valid = a[3];                 // Single bit
assign overflow = b[2:0] > 3'b100;   // Bit range

// Concatenations
wire [7:0] concat_result = {a, b};   // Concatenate two 4-bit vectors
wire [3:0] concat_mixed = {a[2:0], b[3]}; // Mixed concatenation

// ============================================================================
// 8. GATE INSTANTIATIONS
// ============================================================================

// AND gates
and gate_and1 (and_result, a[0], b[0]);
and gate_and2 (and_vec[0], a[1], b[1]);

// OR gates
or gate_or1 (or_result, a[0], b[0]);
or gate_or2 (or_vec[0], a[1], b[1]);

// XOR gates
xor gate_xor1 (xor_result, a[0], b[0]);
xor gate_xor2 (xor_vec[0], a[1], b[1]);

// NOT gates
not gate_not1 (not_result, a[0]);
not gate_not2 (not_vec[0], a[1]);

// NAND gates
nand gate_nand1 (nand_result, a[0], b[0]);

// NOR gates
nor gate_nor1 (nor_result, a[0], b[0]);

// BUF gates
buf gate_buf1 (buf_result, a[0]);

// ============================================================================
// 9. MULTIPLEXER LOGIC
// ============================================================================

// 2-to-1 MUX
assign mux2_1 = sel[0] ? a : b;

// 4-to-1 MUX
assign mux4_1 = (sel == 2'b00) ? a :
                (sel == 2'b01) ? b :
                (sel == 2'b10) ? c :
                d;

// ============================================================================
// 10. COMPARISON OPERATIONS
// ============================================================================

// Equality
wire equal_ab = (a == b);
wire not_equal_cd = (c != d);

// Greater than
wire greater_ab = (a > b);
wire greater_equal_cd = (c >= d);

// Less than
wire less_ab = (a < b);
wire less_equal_cd = (c <= d);

// ============================================================================
// 11. LOGICAL OPERATIONS
// ============================================================================

// Logical AND
wire logical_and = (a > 0) && (b > 0);

// Logical OR
wire logical_or = (a == 0) || (b == 0);

// Logical NOT
wire logical_not = !(a == b);

// ============================================================================
// 12. CONDITIONAL ASSIGNMENTS
// ============================================================================

// If-else style using ternary
assign conditional_result = (enable) ? (a + b) : 4'b0000;

// Multiple conditions
assign multi_conditional = (sel == 2'b00) ? a :
                          (sel == 2'b01) ? b :
                          (sel == 2'b10) ? c :
                          d;

// ============================================================================
// 13. PARAMETERIZED OPERATIONS
// ============================================================================

// Parameter definitions
parameter WIDTH = 4;
parameter DELAY = 2;

// Using parameters
wire [WIDTH-1:0] param_result = a + b;

// ============================================================================
// 14. FUNCTIONAL EXAMPLES
// ============================================================================

// Adder with carry
wire [4:0] adder_result = a + b + c[0];

// Multiplier
wire [7:0] multiplier_result = a * b;

// Comparator
wire [2:0] comparator_result = (a > b) ? 3'b001 :
                               (a < b) ? 3'b010 :
                               3'b100;

// Decoder
wire [3:0] decoder_result = (sel == 2'b00) ? 4'b0001 :
                            (sel == 2'b01) ? 4'b0010 :
                            (sel == 2'b10) ? 4'b0100 :
                            4'b1000;

// Encoder
wire [1:0] encoder_result = (data_in[3]) ? 2'b11 :
                            (data_in[2]) ? 2'b10 :
                            (data_in[1]) ? 2'b01 :
                            2'b00;

// ============================================================================
// 15. COMBINATIONAL LOGIC EXAMPLES
// ============================================================================

// Full adder
wire full_adder_sum = a[0] ^ b[0] ^ c[0];
wire full_adder_cout = (a[0] & b[0]) | (a[0] & c[0]) | (b[0] & c[0]);

// Half adder
wire half_adder_sum = a[0] ^ b[0];
wire half_adder_cout = a[0] & b[0];

// Priority encoder
wire [2:0] priority_encoder = (data_in[7]) ? 3'b111 :
                              (data_in[6]) ? 3'b110 :
                              (data_in[5]) ? 3'b101 :
                              (data_in[4]) ? 3'b100 :
                              (data_in[3]) ? 3'b011 :
                              (data_in[2]) ? 3'b010 :
                              (data_in[1]) ? 3'b001 :
                              3'b000;

// ============================================================================
// 16. FINAL OUTPUT ASSIGNMENTS
// ============================================================================

// Main outputs
assign result1 = (sel == 2'b00) ? sum_ab :
                 (sel == 2'b01) ? diff_cd :
                 (sel == 2'b10) ? {1'b0, a} :
                 {1'b0, b};

assign result2 = (a * b) + (c * d) + (a & b);

assign result3 = (a & b) | (c ^ d);

assign valid = (a > b) ? 1'b1 : 1'b0;

assign overflow = (a + b > 4'b1111) ? 1'b1 : 1'b0;

endmodule

/*
 * SYNTAX SUMMARY:
 * 
 * 1. Module declarations (port list style)
 * 2. Input/Output declarations (vector and scalar)
 * 3. Wire declarations with assignments
 * 4. Arithmetic operations (+, -, *, /)
 * 5. Bitwise operations (&, |, ^, ~)
 * 6. Ternary operators (condition ? value1 : value2)
 * 7. Complex expressions with parentheses
 * 8. Bit selections ([index] and [high:low])
 * 9. Concatenations ({signal1, signal2})
 * 10. Gate instantiations (and, or, xor, not, nand, nor, buf)
 * 11. Comparison operations (==, !=, >, >=, <, <=)
 * 12. Logical operations (&&, ||, !)
 * 13. Conditional assignments
 * 14. Parameter definitions
 * 15. Functional examples (adder, multiplier, comparator, decoder, encoder)
 * 16. Combinational logic examples (full adder, half adder, priority encoder)
 * 
 * All syntax supported by MyLogic EDA Tool unified parser!
 */
