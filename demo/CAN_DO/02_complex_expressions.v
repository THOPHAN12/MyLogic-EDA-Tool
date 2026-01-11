// ============================================================
// CAN_DO Example 2: Complex Combinational Expressions
// ============================================================
// Đây là những gì MyLogic đã làm được:
// - Parse nested expressions với operator precedence
// - Xử lý parentheses matching
// - Synthesis phức tạp thành AIG
// - Optimization các common subexpressions
//
// Status: ✅ FULLY SUPPORTED
// ============================================================

module complex_expressions(
    input a,
    input b,
    input c,
    input d,
    output out1,
    output out2,
    output out3
);

    // Nested expressions với parentheses
    assign out1 = (a & b) | (c & d);
    
    // Complex expression với multiple operators
    assign out2 = a & b & c | d;
    
    // Nested NOT với AND
    assign out3 = ~(a & b);

endmodule

