// ============================================================
// CAN_DO Example 7: Optimization Opportunities
// ============================================================
// Đây là những gì MyLogic đã làm được:
// - Structural Hashing (Strash) - loại bỏ duplicate logic
// - Dead Code Elimination (DCE) - loại bỏ unused logic
// - Common Subexpression Elimination (CSE) - share redundant logic
// - Constant Propagation (ConstProp) - propagate constants
// - Logic Balancing (Balance) - balance logic depth
//
// Status: ✅ FULLY SUPPORTED
// ============================================================

module optimization_example(
    input a,
    input b,
    input c,
    output out1,
    output out2,
    output out3
);

    // Common subexpression: (a & b) xuất hiện 2 lần
    // CSE sẽ tối ưu hóa bằng cách share logic
    wire common = a & b;
    assign out1 = common | c;
    assign out2 = common & c;
    
    // Constant propagation example
    wire const_val = 1'b1;
    assign out3 = a & const_val;  // ConstProp sẽ simplify thành a

endmodule

