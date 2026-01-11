// ============================================================
// CAN_DO Example 6: Arithmetic Operations
// ============================================================
// Đây là những gì MyLogic đã làm được:
// - Multi-bit arithmetic (ADD, SUB)
// - Ripple-carry adder implementation
// - 2's complement subtraction
// - Synthesis multi-bit operations thành AIG
//
// Status: ✅ SUPPORTED (Basic Implementation)
// Note: Advanced algorithms (carry-lookahead, etc.) CHƯA có
// ============================================================

module arithmetic_operations(
    input [3:0] a,
    input [3:0] b,
    output sum0,
    output sum1,
    output sum2,
    output sum3,
    output [3:0] diff,
    output carry_out
);

    // Addition (ripple-carry adder)
    // Split concatenation assignment into separate assignments
    wire [4:0] add_result;
    assign add_result = a + b;
    assign carry_out = add_result[4];
    assign sum0 = add_result[0];
    assign sum1 = add_result[1];
    assign sum2 = add_result[2];
    assign sum3 = add_result[3];
    
    // Subtraction (2's complement)
    assign diff = a - b;

endmodule

