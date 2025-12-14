/*
 * Comprehensive Test - Tất Cả Tính Năng
 * 
 * File này test TẤT CẢ tính năng trong một module:
 * - Parameters
 * - Always blocks (sequential và combinational)
 * - Generate blocks
 * - Case statements
 * - Bit manipulation
 * - Memory
 * - Functions
 * - Module instantiation
 * - Tất cả operations
 */

module full_feature_test #(
    parameter WIDTH = 8,
    parameter DEPTH = 16,
    parameter N = 4
)(
    input signed [WIDTH-1:0] data_in,
    input unsigned [WIDTH-1:0] addr,
    input [N-1:0] control,
    input clk,
    input rst_n,
    input enable,
    output [WIDTH*2-1:0] result,
    output [WIDTH-1:0] mem_out,
    output [WIDTH-1:0] processed_data
);

    // Local parameters
    localparam ADDR_WIDTH = 4;
    
    // Internal signals
    wire signed [WIDTH-1:0] temp1, temp2;
    wire [WIDTH-1:0] temp3, temp4;
    reg signed [WIDTH*2-1:0] result_reg;
    reg [WIDTH-1:0] processed_data_reg;
    
    // Memory
    reg [WIDTH-1:0] memory [0:DEPTH-1];
    
    // Combinational always
    always @(*) begin
        processed_data_reg = (data_in > 8'd100) ? (data_in + 8'd10) : (data_in - 8'd5);
    end
    
    assign temp1 = data_in + 8'd10;
    assign temp2 = data_in - 8'd5;
    assign temp3 = data_in & 8'hFF;
    assign temp4 = data_in | 8'hAA;
    assign processed_data = processed_data_reg;
    
    // Sequential always
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            result_reg <= 0;
        end else if (enable) begin
            result_reg <= {temp1, temp2};
        end
    end
    
    assign result = result_reg;
    
    // Memory operations
    always @(posedge clk) begin
        if (enable) begin
            memory[addr] <= data_in;
        end
    end
    assign mem_out = memory[addr];
    
    // Generate block
    generate
        genvar i;
        for (i = 0; i < N; i = i + 1) begin : gen_loop
            wire [WIDTH-1:0] temp;
            assign temp = data_in[i*2 +: 2];
        end
    endgenerate
    
    // Case statement
    reg [WIDTH-1:0] case_result;
    always @(*) begin
        case (control)
            2'b00: case_result = temp1;
            2'b01: case_result = temp2;
            2'b10: case_result = temp3;
            2'b11: case_result = temp4;
            default: case_result = 8'h00;
        endcase
    end
    
    // Function
    function [WIDTH-1:0] add_func;
        input [WIDTH-1:0] a, b;
        begin
            add_func = a + b;
        end
    endfunction
    
    // Bit manipulation
    wire [WIDTH-1:0] bit_slice = data_in[7:4];
    wire [WIDTH*2-1:0] replicated = {4{data_in}};
    wire [WIDTH*2-1:0] concatenated = {temp1, temp2};
    
endmodule

