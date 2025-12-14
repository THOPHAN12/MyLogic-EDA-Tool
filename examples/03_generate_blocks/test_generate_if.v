/*
 * Test Generate Blocks - If Statements
 * 
 * Test các tính năng:
 * - generate if statements
 * - Conditional generation
 */

module test_generate_if #(
    parameter ENABLE_FEATURE = 1,
    parameter USE_XOR = 0
)(
    input [7:0] a,
    input [7:0] b,
    output [7:0] out
);

    generate
        if (ENABLE_FEATURE == 1) begin : gen_feature
            wire [7:0] feature_out;
            assign feature_out = a ^ b;
            assign out = feature_out;
        end else begin : gen_no_feature
            assign out = a & b;
        end
    endgenerate
    
    generate
        if (USE_XOR) begin : gen_xor
            assign out = a ^ b;
        end
    endgenerate
    
endmodule

