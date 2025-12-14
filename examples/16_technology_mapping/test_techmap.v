/*
 * Test Technology Mapping
 * 
 * Mạch đơn giản để test technology mapping flow:
 * - AND gate
 * - OR gate
 * - XOR gate
 * - Complex function
 */

module test_techmap(
    input a,
    input b,
    input c,
    input d,
    output out1,
    output out2,
    output out3
);

    // Simple gates
    wire temp1 = a & b;
    wire temp2 = c | d;
    
    // XOR
    assign out1 = temp1 ^ temp2;
    
    // Complex function
    assign out2 = (a & b) | (c & d);
    assign out3 = ~(a & b);
    
endmodule

