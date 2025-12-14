/*
 * Test Shift Operations
 * 
 * Test các tính năng:
 * - Left shift (<<)
 * - Right shift (>>)
 * - Arithmetic right shift (>>>)
 */

module test_shift(
    input [7:0] data,
    input [2:0] shift_amount,
    output [7:0] left_shift,
    output [7:0] right_shift,
    output [7:0] arithmetic_shift
);

    assign left_shift = data << shift_amount;
    assign right_shift = data >> shift_amount;
    assign arithmetic_shift = data >>> shift_amount;
    
endmodule

