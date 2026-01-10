/*
 * Test Memory và Arrays
 * 
 * Test các tính năng:
 * - Memory declarations
 * - Array indexing
 * - Parameterized dimensions
 */

module test_memory #(
    parameter WIDTH = 8,
    parameter DEPTH = 16
)(
    input clk,
    input [3:0] addr,
    input [WIDTH-1:0] data_in,
    output [WIDTH-1:0] data_out
);

    // Memory declaration
    reg [WIDTH-1:0] memory [0:DEPTH-1];
    
    // Memory write (sequential)
    always @(posedge clk) begin
        memory[addr] <= data_in;
    end
    
    // Memory read (combinational)
    assign data_out = memory[addr];
    
    // Array of arrays
    reg [WIDTH-1:0] buffer [0:3];
    
    // Array indexing
    wire [WIDTH-1:0] temp = buffer[addr[1:0]];
    
endmodule

