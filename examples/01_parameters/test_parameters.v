/*
 * Test Parameters và Localparams
 * 
 * Test các tính năng:
 * - Module parameters với default values
 * - Parameterized widths
 * - Local parameters
 * - Parameter expressions
 */

module test_parameters #(
    parameter WIDTH = 8,
    parameter DEPTH = 16,
    parameter N = 4,
    parameter MAX_VAL = 255
)(
    input [WIDTH-1:0] data_in,
    input [N-1:0] addr,
    output [WIDTH*2-1:0] result
);

    // Local parameters
    localparam ADDR_WIDTH = 4;
    localparam DATA_WIDTH = WIDTH * 2;
    localparam TOTAL_SIZE = WIDTH * DEPTH;
    
    // Sử dụng parameters trong expressions
    wire [WIDTH-1:0] temp1 = data_in + WIDTH;
    wire [DATA_WIDTH-1:0] temp2 = {data_in, data_in};
    wire [ADDR_WIDTH-1:0] temp3 = addr;
    
    assign result = temp2;
    
endmodule

