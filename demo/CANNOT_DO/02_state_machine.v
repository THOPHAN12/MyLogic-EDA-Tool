// ============================================================
// CANNOT_DO Example 2: State Machine
// ============================================================
// Đây là những gì MyLogic CHƯA làm được:
// - State machine synthesis
// - State encoding và optimization
// - State transition logic
//
// Status: ❌ NOT SUPPORTED
// Reason: State machines yêu cầu sequential logic support
// ============================================================

module state_machine(
    input clk,
    input rst,
    input start,
    output reg [1:0] state
);

    // State machine - CHƯA hỗ trợ
    // MyLogic chưa thể extract và optimize state machines
    localparam IDLE = 2'b00;
    localparam RUN = 2'b01;
    localparam DONE = 2'b10;
    
    always @(posedge clk) begin
        if (rst) begin
            state <= IDLE;
        end else begin
            case (state)
                IDLE: state <= start ? RUN : IDLE;
                RUN: state <= DONE;
                DONE: state <= IDLE;
                default: state <= IDLE;
            endcase
        end
    end

endmodule

