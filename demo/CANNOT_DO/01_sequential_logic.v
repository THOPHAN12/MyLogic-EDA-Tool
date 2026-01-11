// ============================================================
// CANNOT_DO Example 1: Sequential Logic (Flip-flops)
// ============================================================
// Đây là những gì MyLogic CHƯA làm được:
// - Sequential always blocks với clock edges (posedge clk)
// - Flip-flops (D, T, JK, SR)
// - State machines
// - Sequential synthesis và optimization
//
// Status: ❌ NOT SUPPORTED
// Reason: Cần xử lý timing, state, clock domains - độ phức tạp cao
// ============================================================

module sequential_logic(
    input clk,
    input rst,
    input d,
    output reg q
);

    // Sequential always block - CHƯA hỗ trợ đầy đủ
    // MyLogic chưa thể synthesis flip-flops
    always @(posedge clk) begin
        if (rst) begin
            q <= 1'b0;
        end else begin
            q <= d;
        end
    end

endmodule

