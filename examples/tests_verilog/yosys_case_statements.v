// Test case: Case statements parsing
module case_test(
    input [1:0] sel,
    input a, b, c, d,
    output reg out1,
    output reg [1:0] out2
);

    // Simple case statement
    always @(*) begin
        case (sel)
            2'b00: out1 = a;
            2'b01: out1 = b;
            2'b10: out1 = c;
            default: out1 = d;
        endcase
    end

    // Case with ranges
    always @(*) begin
        case (sel)
            0: out2 = 2'b00;
            1: out2 = 2'b01;
            2: out2 = 2'b10;
            3: out2 = 2'b11;
            default: out2 = 2'b00;
        endcase
    end

endmodule

