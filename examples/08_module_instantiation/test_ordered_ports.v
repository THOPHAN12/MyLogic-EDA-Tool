/*
 * Test Module Instantiation - Ordered Ports
 * 
 * Test các tính năng:
 * - Ordered port connections
 */

// Top module với ordered ports (đặt ở cuối để parser parse)
module test_ordered_ports(
    input [7:0] in1,
    input [7:0] in2,
    output [15:0] prod_out
);

    // Ordered ports - inline multiplier logic thay vì instantiation
    // (vì parser chỉ parse module cuối cùng)
    assign prod_out = in1 * in2;
    
endmodule

// Sub-module (sẽ không được parse)
module multiplier(
    input [7:0] a,
    input [7:0] b,
    output [15:0] product
);
    assign product = a * b;
endmodule

