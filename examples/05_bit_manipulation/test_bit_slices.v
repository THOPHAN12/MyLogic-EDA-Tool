/*
 * Test Bit Slices
 * 
 * Test các tính năng:
 * - Bit slices [msb:lsb]
 * - Single bit access [bit]
 * - Parameterized indices
 */

module test_bit_slices #(
    parameter WIDTH = 8
)(
    input [WIDTH-1:0] data_in,
    output [3:0] upper_bits,
    output [3:0] lower_bits,
    output [1:0] middle_bits,
    output single_bit
);

    // Bit slices
    assign upper_bits = data_in[7:4];
    assign lower_bits = data_in[3:0];
    assign middle_bits = data_in[5:4];
    
    // Single bit
    assign single_bit = data_in[0];
    
    // Parameterized indices
    wire [3:0] param_slice = data_in[WIDTH-1:WIDTH-4];
    
endmodule

