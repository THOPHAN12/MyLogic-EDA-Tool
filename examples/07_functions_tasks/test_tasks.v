/*
 * Test Tasks
 * 
 * Test các tính năng:
 * - Task declarations
 * - Task calls
 */

module test_tasks(
    input clk,
    input rst
);

    reg [7:0] counter;
    
    // Task declaration
    task reset_counter;
        begin
            counter = 8'd0;
        end
    endtask
    
    // Task với parameters
    task increment_counter;
        input [7:0] inc;
        begin
            counter = counter + inc;
        end
    endtask
    
    // Task call
    always @(posedge clk) begin
        if (rst) begin
            reset_counter;
        end else begin
            increment_counter(1);
        end
    end
    
endmodule

