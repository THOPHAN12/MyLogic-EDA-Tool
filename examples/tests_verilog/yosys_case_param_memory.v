// Test case: Parameterized memory declarations
module param_memory #(
    parameter WIDTH = 8,
    parameter DEPTH = 256
)(
    input clk,
    input [7:0] addr,
    input [WIDTH-1:0] data_in,
    input we,
    output [WIDTH-1:0] data_out
);

    // Parameterized memory: reg [WIDTH-1:0] mem [DEPTH-1:0];
    reg [WIDTH-1:0] mem [DEPTH-1:0];
    
    // Memory read với bit select
    assign data_out = mem[addr];
    
    // Memory write
    always @(posedge clk) begin
        if (we) begin
            mem[addr] <= data_in;
        end
    end

endmodule

