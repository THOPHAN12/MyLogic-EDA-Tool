/*
 * Test Always Blocks - Sequential Logic
 * 
 * Test các tính năng:
 * - always @(posedge clk)
 * - always @(negedge clk)
 * - always @(posedge clk or negedge rst)
 * - Nonblocking assignments (<=)
 */

module test_always_sequential(
    input clk,
    input rst_n,
    input enable,
    input [7:0] data_in,
    output [7:0] q,
    output [7:0] q2
);

    reg [7:0] q_reg, q2_reg;
    
    // Sequential với posedge clock
    always @(posedge clk) begin
        if (rst_n) begin
            q_reg <= 8'd0;
        end else if (enable) begin
            q_reg <= data_in;
        end
    end
    
    // Sequential với negedge clock
    always @(negedge clk) begin
        q2_reg <= data_in + 1;
    end
    
    assign q = q_reg;
    assign q2 = q2_reg;
    
endmodule

