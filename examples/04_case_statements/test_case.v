/*
 * Test Case Statements
 * 
 * Test các tính năng:
 * - case statements
 * - casex statements
 * - casez statements
 * - default cases
 */

module test_case(
    input [1:0] sel,
    input [7:0] a,
    input [7:0] b,
    input [7:0] c,
    input [7:0] d,
    output [7:0] out,
    output [7:0] outx,
    output [7:0] outz
);

    reg [7:0] out_reg, outx_reg, outz_reg;
    
    // Standard case
    always @(*) begin
        case (sel)
            2'b00: out_reg = a;
            2'b01: out_reg = b;
            2'b10: out_reg = c;
            2'b11: out_reg = d;
            default: out_reg = 8'd0;
        endcase
    end
    
    // Casex (don't care)
    always @(*) begin
        casex (sel)
            2'b0x: outx_reg = a;
            2'b1x: outx_reg = b;
            default: outx_reg = 8'd0;
        endcase
    end
    
    // Casez (high impedance)
    always @(*) begin
        casez (sel)
            2'b0?: outz_reg = a;
            2'b1?: outz_reg = b;
            default: outz_reg = 8'd0;
        endcase
    end
    
    assign out = out_reg;
    assign outx = outx_reg;
    assign outz = outz_reg;
    
endmodule
