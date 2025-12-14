/*
 * Unoptimized Circuit - Cần Tối Ưu
 * 
 * Vấn đề:
 * - Redundant expressions
 * - Common subexpressions không được share
 * - Unused signals
 * - Constants chưa được simplify
 */

module unoptimized(
    input [7:0] a,
    input [7:0] b,
    input [7:0] c,
    output [7:0] out1,
    output [7:0] out2,
    output [7:0] out3
);

    // Vấn đề: Tính a+b nhiều lần
    wire [7:0] temp1 = a + b;
    wire [7:0] temp2 = a + b;  // Duplicate!
    wire [7:0] temp3 = a + b;  // Duplicate!
    
    // Vấn đề: Constants chưa được simplify
    wire [7:0] zero = 8'd0;
    wire [7:0] temp4 = temp1 + zero;  // temp1 + 0 = temp1
    
    // Vấn đề: Unused signals
    wire [7:0] unused = a * b;
    
    // Outputs
    assign out1 = temp1 + c;
    assign out2 = temp2 + c;  // Redundant
    assign out3 = temp4 + c;  // Redundant
    
endmodule

