// Test case: Array indexing với expressions
module array_indexing_test(
    input [7:0] addr1,
    input [7:0] addr2,
    input [7:0] data_in,
    output [7:0] data_out1,
    output [7:0] data_out2,
    output single_bit
);

    // Memory declarations
    reg [7:0] mem1 [0:255];
    reg [7:0] mem2 [0:127];
    
    // Array indexing với simple address
    assign data_out1 = mem1[addr1];
    
    // Array indexing với expression
    assign data_out2 = mem2[addr1 + addr2];
    
    // Array indexing với bit select
    assign single_bit = mem1[addr1][0];

endmodule

