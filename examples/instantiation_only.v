/*
 * Module Instantiation Only
 * MyLogic EDA Tool - Module Hierarchy Support
 */

module main_module(
    input [3:0] data_a, data_b,
    input select,
    output [3:0] result
);
    
    // Instantiate mux2to1 (assume it's defined elsewhere)
    mux2to1 mux_inst (.a(data_a), .b(data_b), .sel(select), .out(result));
    
    // Another instantiation
    alu alu_inst (.a(data_a), .b(data_b), .op(2'b00), .result(result));
endmodule
