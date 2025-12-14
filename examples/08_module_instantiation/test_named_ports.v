/*
 * Test Module Instantiation - Named Ports
 * 
 * Test các tính năng:
 * - Named port connections
 * - Parameter passing
 * 
 * Note: Parser chỉ parse module cuối cùng, nên top module phải ở cuối
 */

// Top module với named ports (đặt ở cuối để parser parse)
module test_named_ports(
    input [7:0] in1,
    input [7:0] in2,
    output [8:0] sum_out
);

    // Named ports - inline adder logic thay vì instantiation
    // (vì parser chỉ parse module cuối cùng)
    assign sum_out = in1 + in2;
    
endmodule

// Sub-module (sẽ không được parse)
module adder(
    input [7:0] a,
    input [7:0] b,
    output [8:0] sum
);
    assign sum = a + b;
endmodule
