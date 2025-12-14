/*
 * Test Logical Operations
 * 
 * Test các tính năng:
 * - Logical AND (&&)
 * - Logical OR (||)
 * - Logical NOT (!)
 */

module test_logical(
    input [7:0] a,
    input [7:0] b,
    output and_result,
    output or_result,
    output not_result
);

    assign and_result = (a > 8'd50) && (b > 8'd50);
    assign or_result = (a == 8'd0) || (b == 8'd0);
    assign not_result = !(a == b);
    
endmodule

