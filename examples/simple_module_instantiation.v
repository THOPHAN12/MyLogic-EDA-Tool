/*
 * Simple Module Instantiation Example
 * MyLogic EDA Tool - Module Hierarchy Support
 */

// 2-to-1 Multiplexer Module
module mux2to1(
    input [3:0] a, b,
    input sel,
    output [3:0] out
);
    assign out = sel ? b : a;
endmodule

// Main module with instantiation
module main_module(
    input [3:0] data_a, data_b,
    input select,
    output [3:0] result
);
    
    // Instantiate mux2to1
    mux2to1 mux_inst (.a(data_a), .b(data_b), .sel(select), .out(result));
endmodule
