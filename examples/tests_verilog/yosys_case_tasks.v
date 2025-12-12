// Test case: Task declarations và calls
module task_test(
    input clk,
    input [7:0] data_in,
    output reg [7:0] data_out
);

    // Task declaration
    task write_data;
        input [7:0] data;
        begin
            data_out = data;
        end
    endtask
    
    // Task call trong always block
    always @(posedge clk) begin
        write_data(data_in);
    end
    
    // Automatic task
    task automatic reset_task;
        begin
            data_out = 8'b0;
        end
    endtask

endmodule

