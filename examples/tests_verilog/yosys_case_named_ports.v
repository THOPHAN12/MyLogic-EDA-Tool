// Test case: Named ports parsing
module named_ports_test(
    input clk,
    input rst,
    input [7:0] data_in,
    output [7:0] data_out
);

    // Simple named ports
    adder add1 (
        .a(data_in[3:0]),
        .b(data_in[7:4]),
        .sum(data_out[3:0])
    );
    
    // Named ports với expressions
    mux mux1 (
        .sel(rst),
        .in0({4{1'b0}}),
        .in1(data_in),
        .out(data_out[7:4])
    );
    
    // Mixed named và ordered ports (nếu hỗ trợ)
    // reg_file rf1 (
    //     data_in,
    //     .addr(data_in[3:0]),
    //     .data_out(data_out)
    // );

endmodule

// Simple adder module for testing
module adder(
    input [3:0] a,
    input [3:0] b,
    output [3:0] sum
);
    assign sum = a + b;
endmodule

// Simple mux module for testing
module mux(
    input sel,
    input [7:0] in0,
    input [7:0] in1,
    output [7:0] out
);
    assign out = sel ? in1 : in0;
endmodule

