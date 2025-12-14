/*
 * Test Replication và Concatenation
 * 
 * Test các tính năng:
 * - Replication {n{signal}}
 * - Concatenation {a, b, c}
 * - Nested replication
 */

module test_replication(
    input [7:0] a,
    input [7:0] b,
    input [3:0] c,
    output [15:0] replicated,
    output [19:0] concatenated,
    output [23:0] nested
);

    // Replication
    assign replicated = {2{a}};  // {a, a}
    
    // Concatenation
    assign concatenated = {a, b, c};
    
    // Nested replication trong concatenation
    assign nested = {{2{a}}, {4{b[1:0]}}};
    
endmodule

