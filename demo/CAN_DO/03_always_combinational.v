module always_combinational(
    input a,
    input b,
    input c,
    output reg out1,
    output reg out2,
    output reg out3
);

    // Combinational always block
    always @(*) begin
        out1 = a & b;
        out2 = (a | b) & c;
        out3= a & b & c;
    end

endmodule

