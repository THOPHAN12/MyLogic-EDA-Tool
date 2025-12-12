// Test case: Memory declarations và array indexing
module memory_test(
    input clk,
    input [7:0] addr,
    input [7:0] data_in,
    input we,  // write enable
    output [7:0] data_out
);

    // Memory declaration: reg [7:0] mem [0:255];
    reg [7:0] mem [0:255];
    
    // Memory read
    assign data_out = mem[addr];
    
    // Memory write (trong always block)
    always @(posedge clk) begin
        if (we) begin
            mem[addr] <= data_in;
        end
    end

endmodule

