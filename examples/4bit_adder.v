/*
 * 4-bit Full Adder
 * 
 * Implements a 4-bit ripple-carry adder using full adder modules.
 * This example is used for testing synthesis and optimization algorithms.
 */

module full_adder_1bit(a, b, cin, sum, cout);
    input a, b, cin;
    output sum, cout;
    
    // Sum = a XOR b XOR cin
    assign sum = a ^ b ^ cin;
    
    // Carry out = (a AND b) OR (cin AND (a XOR b))
    assign cout = (a & b) | (cin & (a ^ b));
endmodule

module adder_4bit(a, b, cin, sum, cout);
    input [3:0] a, b;
    input cin;
    output [3:0] sum;
    output cout;
    
    wire [3:0] carry;
    
    // First full adder
    full_adder_1bit fa0(
        .a(a[0]),
        .b(b[0]),
        .cin(cin),
        .sum(sum[0]),
        .cout(carry[0])
    );
    
    // Second full adder
    full_adder_1bit fa1(
        .a(a[1]),
        .b(b[1]),
        .cin(carry[0]),
        .sum(sum[1]),
        .cout(carry[1])
    );
    
    // Third full adder
    full_adder_1bit fa2(
        .a(a[2]),
        .b(b[2]),
        .cin(carry[1]),
        .sum(sum[2]),
        .cout(carry[2])
    );
    
    // Fourth full adder
    full_adder_1bit fa3(
        .a(a[3]),
        .b(b[3]),
        .cin(carry[2]),
        .sum(sum[3]),
        .cout(cout)
    );
endmodule

