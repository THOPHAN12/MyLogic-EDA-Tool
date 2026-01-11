// ============================================================
// CAN_DO Example 4: Case Statements (MUX Conversion)
// ============================================================
// Đây là những gì MyLogic đã làm được:
// - Parse case statements
// - Convert case statements thành MUX trees
// - Synthesis MUX logic thành AIG
//
// Status: ✅ FULLY SUPPORTED
// ============================================================

module case_statements(
    input [1:0] sel,
    input in0,
    input in1,
    input in2,
    input in3,
    output reg out
);

    always @(*) begin
        case (sel)
            2'b00: out = in0;
            2'b01: out = in1;
            2'b10: out = in2;
            2'b11: out = in3;
            default: out = 1'b0;
        endcase
    end

endmodule

