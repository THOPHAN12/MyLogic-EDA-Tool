// Test case: Bit slices parsing
module bit_slices_test(
    input [7:0] data,
    input [3:0] addr,
    output [3:0] low_bits,
    output [3:0] high_bits,
    output single_bit
);

    // Bit slice với range
    assign low_bits = data[3:0];
    assign high_bits = data[7:4];
    
    // Single bit index
    assign single_bit = data[0];
    
    // Bit slice trong expression
    wire [1:0] temp;
    assign temp = data[5:4] & addr[1:0];

endmodule

