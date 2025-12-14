/*
 * Optimized Circuit - Đã Tối Ưu
 * 
 * Tối ưu:
 * - Common subexpression elimination (CSE)
 * - Constant propagation
 * - Dead code elimination
 */

module optimized(
    input [7:0] a,
    input [7:0] b,
    input [7:0] c,
    output [7:0] out1,
    output [7:0] out2,
    output [7:0] out3
);

    // Tối ưu: Tính a+b một lần (CSE)
    wire [7:0] a_plus_b = a + b;
    
    // Tối ưu: Constants đã được simplify
    // temp1 + 0 = temp1 → a_plus_b
    
    // Tối ưu: Unused signals đã bị loại bỏ (DCE)
    
    // Outputs - sử dụng shared expression
    assign out1 = a_plus_b + c;
    assign out2 = a_plus_b + c;  // Có thể được CSE optimize
    assign out3 = a_plus_b + c;  // Có thể được CSE optimize
    
endmodule

