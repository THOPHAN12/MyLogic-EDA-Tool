// Test case: Parameter expressions
module param_expressions #(
    parameter N = 4,
    parameter M = 8
)(
    input [N-1:0] a,
    input [M-1:0] b,
    output [N+M-1:0] sum
);
    localparam TOTAL = N + M;
    localparam HALF = M / 2;
    localparam OFFSET = N - 1;
    
    wire [TOTAL-1:0] temp;
    wire [HALF-1:0] partial;
    
    assign temp = {a, b};
    assign partial = b[HALF-1:0];
    assign sum = temp;
endmodule

