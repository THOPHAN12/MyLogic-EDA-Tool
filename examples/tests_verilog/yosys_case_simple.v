// Test case: Simple case statement
module case_simple(
    input [1:0] sel,
    input a, b, c,
    output reg out
);

    always @(*) begin
        case (sel)
            2'b00: out = a;
            2'b01: out = b;
            2'b10: out = c;
            default: out = 1'b0;
        endcase
    end

endmodule

