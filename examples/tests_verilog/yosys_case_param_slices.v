// Test case: Parameterized bit slices
module param_slices #(
    parameter WIDTH = 8,
    parameter OFFSET = 4
)(
    input [WIDTH-1:0] data,
    output [OFFSET-1:0] low_bits,
    output [WIDTH-OFFSET-1:0] high_bits
);

    // Parameterized bit slices
    assign low_bits = data[OFFSET-1:0];
    assign high_bits = data[WIDTH-1:OFFSET];
    
    // Replication với parameter
    wire [WIDTH*2-1:0] doubled;
    assign doubled = {WIDTH{data}};

endmodule

