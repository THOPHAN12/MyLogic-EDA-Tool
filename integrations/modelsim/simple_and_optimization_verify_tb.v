`timescale 1ns/1ps

module simple_and_optimization_verify_tb;

  reg a;
  reg b;

  wire out_orig;
  wire out_mapped;

  // Original design
  simple_and_optimization_verify_original dut_original(
    .a(a),
    .b(b),
    .out(out_orig)
  );

  // Mapped design
  simple_and_optimization_verify_mapped dut_mapped(
    .a(a),
    .b(b),
    .out(out_mapped)
  );

  initial begin
    $display("========================================");
    $display("ModelSim Verification Testbench");
    $display("========================================");

    // Test 1
    $display("\nTest 1:");
    a = 0;
    b = 0;
    #10;  // Wait for propagation
    $display("  out_orig = %b, out_mapped = %b", out_orig, out_mapped);
    if (
(out_orig == out_mapped)
    ) begin
      $display("  [PASS] Test 1 passed");
    end else begin
      $display("  [FAIL] Test 1 failed - outputs don't match");
      if (out_orig != out_mapped)
        $display("    out: original=%b, mapped=%b", out_orig, out_mapped);
    end

    // Test 2
    $display("\nTest 2:");
    a = 0;
    b = 1;
    #10;  // Wait for propagation
    $display("  out_orig = %b, out_mapped = %b", out_orig, out_mapped);
    if (
(out_orig == out_mapped)
    ) begin
      $display("  [PASS] Test 2 passed");
    end else begin
      $display("  [FAIL] Test 2 failed - outputs don't match");
      if (out_orig != out_mapped)
        $display("    out: original=%b, mapped=%b", out_orig, out_mapped);
    end

    // Test 3
    $display("\nTest 3:");
    a = 1;
    b = 0;
    #10;  // Wait for propagation
    $display("  out_orig = %b, out_mapped = %b", out_orig, out_mapped);
    if (
(out_orig == out_mapped)
    ) begin
      $display("  [PASS] Test 3 passed");
    end else begin
      $display("  [FAIL] Test 3 failed - outputs don't match");
      if (out_orig != out_mapped)
        $display("    out: original=%b, mapped=%b", out_orig, out_mapped);
    end

    // Test 4
    $display("\nTest 4:");
    a = 1;
    b = 1;
    #10;  // Wait for propagation
    $display("  out_orig = %b, out_mapped = %b", out_orig, out_mapped);
    if (
(out_orig == out_mapped)
    ) begin
      $display("  [PASS] Test 4 passed");
    end else begin
      $display("  [FAIL] Test 4 failed - outputs don't match");
      if (out_orig != out_mapped)
        $display("    out: original=%b, mapped=%b", out_orig, out_mapped);
    end

    $display("\n========================================");
    $display("Simulation completed");
    $display("========================================");
    $finish;
  end

endmodule