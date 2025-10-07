/*
 * Duplicate nodes test case for Strash algorithm
 * Contains duplicate logic that should be optimized
 */

module duplicate_nodes (
    input a,
    input b,
    input c,
    output out1,
    output out2
);

// Duplicate AND gates
assign temp1 = a & b;
assign temp2 = a & b;  // Duplicate of temp1

// Duplicate OR gates  
assign out1 = temp1 | c;
assign out2 = temp2 | c;  // Duplicate of out1 logic

endmodule
