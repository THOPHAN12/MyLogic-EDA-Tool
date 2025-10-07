/*
 * Sequential Circuit Example - 4-bit Counter
 * MyLogic EDA Tool Sequential Circuit Support
 * 
 * Ví dụ về mạch tuần tự: 4-bit counter với reset
 */

module counter_4bit (
    input CLK,        // Clock signal
    input RST,        // Reset signal
    input EN,         // Enable signal
    output reg [3:0] Q,  // 4-bit counter output
    output CO         // Carry out
);

// Sequential logic với DFF
always @(posedge CLK or posedge RST) begin
    if (RST) begin
        Q <= 4'b0000;  // Reset to 0
    end else if (EN) begin
        Q <= Q + 1;    // Increment counter
    end
end

// Combinational logic cho carry out
assign CO = (Q == 4'b1111) ? 1'b1 : 1'b0;

endmodule

/*
 * Sequential Circuit Example - Shift Register
 */
module shift_register (
    input CLK,        // Clock signal
    input RST,        // Reset signal
    input SI,         // Serial input
    output SO,        // Serial output
    output reg [3:0] Q  // Parallel output
);

// Sequential logic với DFF
always @(posedge CLK or posedge RST) begin
    if (RST) begin
        Q <= 4'b0000;  // Reset to 0
    end else begin
        Q <= {Q[2:0], SI};  // Shift left với serial input
    end
end

// Combinational logic cho serial output
assign SO = Q[3];

endmodule

/*
 * Sequential Circuit Example - State Machine
 */
module state_machine (
    input CLK,        // Clock signal
    input RST,        // Reset signal
    input A, B,       // Input signals
    output reg [1:0] STATE,  // Current state
    output reg Y      // Output signal
);

// State encoding
localparam S0 = 2'b00;
localparam S1 = 2'b01;
localparam S2 = 2'b10;
localparam S3 = 2'b11;

// Sequential logic với DFF
always @(posedge CLK or posedge RST) begin
    if (RST) begin
        STATE <= S0;  // Reset to state 0
    end else begin
        case (STATE)
            S0: STATE <= A ? S1 : S0;
            S1: STATE <= B ? S2 : S0;
            S2: STATE <= A ? S3 : S1;
            S3: STATE <= B ? S0 : S2;
            default: STATE <= S0;
        endcase
    end
end

// Combinational logic cho output
always @(*) begin
    case (STATE)
        S0: Y = 1'b0;
        S1: Y = 1'b0;
        S2: Y = 1'b1;
        S3: Y = 1'b1;
        default: Y = 1'b0;
    endcase
end

endmodule
