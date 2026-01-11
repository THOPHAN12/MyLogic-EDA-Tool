// ============================================================
// CANNOT_DO Example 3: Memory Arrays (Full Support)
// ============================================================
// Đây là những gì MyLogic CHƯA làm được đầy đủ:
// - Memory array synthesis và optimization
// - Memory inference và mapping
// - RAM/ROM synthesis
//
// Status: ⚠️ PARTIALLY SUPPORTED
// Note: Parser có thể parse memory arrays nhưng synthesis
//       và optimization chưa được hỗ trợ đầy đủ
// ============================================================

module memory_arrays(
    input clk,
    input [3:0] addr,
    input [7:0] data_in,
    input we,
    output reg [7:0] data_out
);

    // Memory array - CHƯA hỗ trợ synthesis đầy đủ
    // MyLogic parser có thể parse nhưng không thể synthesis
    // thành memory structures hoặc optimize memory access
    reg [7:0] memory [0:15];
    
    always @(posedge clk) begin
        if (we) begin
            memory[addr] <= data_in;
        end
        data_out <= memory[addr];
    end

endmodule

