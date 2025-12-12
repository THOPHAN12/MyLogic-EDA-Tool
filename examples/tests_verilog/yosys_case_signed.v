// Test case: Signed/unsigned declarations
module signed_test(
    input signed [7:0] data_in,
    input unsigned [3:0] addr,
    output signed [15:0] result
);
    wire signed [7:0] temp;
    wire unsigned [3:0] count;
    reg signed [15:0] accumulator;
    
    assign temp = data_in;
    assign count = addr;
    assign result = accumulator;
endmodule

