module complex_expressions(
    input a,
    input b,
    input c,
    input d,
    output out1,
    output out2,
    output out3
);

    // Nested expressions với parentheses
    assign out1 = (a & b) | (c & d);
    
    // Complex expression với multiple operators
    assign out2 = a & b & c | d;
    
    // Nested NOT với AND
    assign out3 = ~(a & b);

endmodule
