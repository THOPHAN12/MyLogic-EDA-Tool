/*
 * Dead code test case for DCE algorithm
 * Contains unused logic that should be removed
 */

module dead_code (
    input a,
    input b,
    input c,
    output out
);

// Used logic
assign temp1 = a & b;
assign out = temp1 | c;

// Dead code - not connected to any output
assign dead1 = a ^ b;
assign dead2 = dead1 & c;
assign dead3 = dead2 | a;

endmodule
