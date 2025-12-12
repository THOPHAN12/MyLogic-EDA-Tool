// Test case: Replication parsing
module replication_test(
    input [3:0] a,
    input [3:0] b,
    output [15:0] padded,
    output [7:0] zeros,
    output [11:0] repeated
);

    // Replication đơn giản
    assign zeros = {4{1'b0}};
    
    // Replication với signal
    assign repeated = {3{a}};
    
    // Replication trong concatenation
    assign padded = {a, {4{1'b0}}, b};

endmodule

