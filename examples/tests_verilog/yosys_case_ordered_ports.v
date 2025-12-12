// Test case: Ordered ports parsing với expressions
module ordered_ports_test(
    input [7:0] a,
    input [7:0] b,
    output [7:0] sum,
    output [7:0] diff
);

    // Ordered ports với simple signals
    adder add1 (a, b, sum);
    
    // Ordered ports với bit slices
    subtractor sub1 (a[7:4], b[7:4], diff[7:4]);
    
    // Ordered ports với concatenation
    concat_module concat1 ({a[3:0], b[3:0]}, {a[7:4], b[7:4]}, diff[3:0]);

endmodule

// Simple subtractor module
module subtractor(
    input [3:0] a,
    input [3:0] b,
    output [3:0] diff
);
    assign diff = a - b;
endmodule

// Simple concat module
module concat_module(
    input [7:0] in1,
    input [7:0] in2,
    output [7:0] out
);
    assign out = in1 & in2;
endmodule

