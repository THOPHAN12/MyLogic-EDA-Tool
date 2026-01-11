// ============================================================
// CAN_DO Example 3: Combinational Always Blocks
// ============================================================
// Đây là những gì MyLogic đã làm được:
// - Parse always @(*) blocks (combinational logic)
// - Convert always blocks thành assign statements
// - Synthesis combinational logic trong always blocks
//
// Status: ✅ FULLY SUPPORTED
// Note: Sequential always blocks (posedge clk) CHƯA hỗ trợ đầy đủ
// ============================================================

module always_combinational(
    input a,
    input b,
    input c,
    output reg out1,
    output reg out2
);

    // Combinational always block
    always @(*) begin
        out1 = a & b;
        out2 = (a | b) & c;
    end

endmodule

