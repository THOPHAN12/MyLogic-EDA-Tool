/*
 * Test Functions
 * 
 * Test các tính năng:
 * - Function declarations
 * - Function calls
 * - Parameterized widths
 * - Signed functions
 */

module test_functions(
    input [7:0] a,
    input [7:0] b,
    output [7:0] result1,
    output [7:0] result2
);

    // Function với return width
    function [7:0] add;
        input [7:0] x, y;
        begin
            add = x + y;
        end
    endfunction
    
    // Function signed
    function signed [7:0] signed_add;
        input signed [7:0] x, y;
        begin
            signed_add = x + y;
        end
    endfunction
    
    // Function calls
    assign result1 = add(a, b);
    assign result2 = signed_add(a, b);
    
endmodule

