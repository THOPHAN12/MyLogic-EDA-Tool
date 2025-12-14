/*
 * Test Comparison Operations
 * 
 * Test các tính năng:
 * - Greater than (>)
 * - Less than (<)
 * - Equal (==)
 * - Not equal (!=)
 * - Greater or equal (>=)
 * - Less or equal (<=)
 */

module test_comparison(
    input [7:0] a,
    input [7:0] b,
    output gt,
    output lt,
    output eq,
    output ne,
    output ge,
    output le
);

    assign gt = a > b;
    assign lt = a < b;
    assign eq = a == b;
    assign ne = a != b;
    assign ge = a >= b;
    assign le = a <= b;
    
endmodule

