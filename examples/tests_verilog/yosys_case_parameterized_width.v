// Test case: Parameterized widths
module parameterized_width #(
    parameter WIDTH = 8,
    parameter DEPTH = 16
)(
    input [WIDTH-1:0] data_in,
    input [DEPTH-1:0] addr,
    output [WIDTH*2-1:0] result
);
    localparam DOUBLE_WIDTH = WIDTH * 2;
    wire [WIDTH-1:0] temp;
    wire [DOUBLE_WIDTH-1:0] expanded;
    
    assign temp = data_in;
    assign expanded = {temp, temp};
    assign result = expanded;
endmodule

