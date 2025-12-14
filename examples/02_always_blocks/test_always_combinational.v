/*
 * Test Always Blocks - Combinational Logic
 * 
 * Test các tính năng:
 * - always @(*)
 * - Blocking assignments (=)
 * - If-else statements
 */

module test_always_combinational(
    input [7:0] a,
    input [7:0] b,
    input sel,
    output [7:0] out
);

    // Combinational always block với ternary operator để tránh validation error
    reg [7:0] out_reg;
    always @(*) begin
        out_reg = sel ? (a + b) : (a - b);
    end
    
    // Assign output
    assign out = out_reg;
    
endmodule

