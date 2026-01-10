`timescale 1ns/1ps

module test_memory_tb;

    reg clk;
    reg [3:0] addr;
    reg [7:0] data_in;
    wire [7:0] data_out;

    // Instantiate DUT
    test_memory #(
        .WIDTH(8),
        .DEPTH(16)
    ) dut (
        .clk(clk),
        .addr(addr),
        .data_in(data_in),
        .data_out(data_out)
    );

    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    initial begin
        $display("========================================");
        $display("Test Memory Module Simulation");
        $display("========================================");
        $display("");

        // Initialize
        addr = 0;
        data_in = 0;
        #10;

        // Test 1: Write and read at address 0
        $display("Test 1: Write 0xAA to address 0");
        addr = 0;
        data_in = 8'hAA;
        #10;  // Wait for clock
        @(posedge clk);
        #5;
        $display("  Address: %d, Data written: 0x%02h, Data read: 0x%02h", addr, data_in, data_out);
        if (data_out == 8'hAA) begin
            $display("  [PASS] Test 1 passed");
        end else begin
            $display("  [FAIL] Test 1 failed - expected 0xAA, got 0x%02h", data_out);
        end
        $display("");

        // Test 2: Write and read at address 5
        $display("Test 2: Write 0x55 to address 5");
        addr = 5;
        data_in = 8'h55;
        #10;
        @(posedge clk);
        #5;
        $display("  Address: %d, Data written: 0x%02h, Data read: 0x%02h", addr, data_in, data_out);
        if (data_out == 8'h55) begin
            $display("  [PASS] Test 2 passed");
        end else begin
            $display("  [FAIL] Test 2 failed - expected 0x55, got 0x%02h", data_out);
        end
        $display("");

        // Test 3: Write and read at address 15
        $display("Test 3: Write 0xFF to address 15");
        addr = 15;
        data_in = 8'hFF;
        #10;
        @(posedge clk);
        #5;
        $display("  Address: %d, Data written: 0x%02h, Data read: 0x%02h", addr, data_in, data_out);
        if (data_out == 8'hFF) begin
            $display("  [PASS] Test 3 passed");
        end else begin
            $display("  [FAIL] Test 3 failed - expected 0xFF, got 0x%02h", data_out);
        end
        $display("");

        // Test 4: Verify memory retention at different address
        // Read from address 5 (should still have 0x55 from Test 2)
        $display("Test 4: Read from address 5 (should retain 0x55 from Test 2)");
        addr = 5;  // Read from address 5 (not written in Test 3)
        #5;  // Small delay for combinational read path
        $display("  Address: %d, Data read: 0x%02h", addr, data_out);
        if (data_out == 8'h55) begin
            $display("  [PASS] Test 4 passed - memory retained data");
        end else begin
            $display("  [FAIL] Test 4 failed - expected 0x55, got 0x%02h", data_out);
        end
        $display("");

        $display("========================================");
        $display("Simulation completed");
        $display("========================================");
        
        #100;
        $finish;
    end

endmodule
