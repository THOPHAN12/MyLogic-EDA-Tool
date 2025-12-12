// Test case: Function declarations và calls
module function_test(
    input [7:0] a,
    input [7:0] b,
    output [7:0] sum,
    output [7:0] max_val
);

    // Function declaration
    function [7:0] add;
        input [7:0] x;
        input [7:0] y;
        begin
            add = x + y;
        end
    endfunction
    
    // Function call trong assign
    assign sum = add(a, b);
    
    // Function với signed
    function signed [7:0] maximum;
        input signed [7:0] x;
        input signed [7:0] y;
        begin
            maximum = (x > y) ? x : y;
        end
    endfunction
    
    assign max_val = maximum(a, b);

endmodule

