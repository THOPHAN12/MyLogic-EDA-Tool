module generate_blocks(
    input in0,
    input in1,
    input in2,
    input in3,
    input in4,
    input in5,
    input in6,
    input in7,
    input enable,
    output out0,
    output out1,
    output out2,
    output out3,
    output out4,
    output out5,
    output out6,
    output out7
);

    // Generate blocks are unrolled into explicit assign statements
    // This is equivalent to: generate for (i = 0; i < 8; i = i + 1) assign out[i] = in[i] & enable;
    assign out0 = in0 & enable;
    assign out1 = in1 & enable;
    assign out2 = in2 & enable;
    assign out3 = in3 & enable;
    assign out4 = in4 & enable;
    assign out5 = in5 & enable;
    assign out6 = in6 & enable;
    assign out7 = in7 & enable;

endmodule

