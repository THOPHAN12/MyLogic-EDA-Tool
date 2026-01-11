`timescale 1ns/1ps

module always_combinational_synthesis_verify_tb;

  reg a;
  reg b;
  reg c;

  wire out1_orig;
  wire out1_mapped;
  wire out2_orig;
  wire out2_mapped;

  // Original design
  always_combinational_synthesis_verify_original dut_original(
    .a(a),
    .b(b),
    .c(c),
    .out1(out1_orig),
    .out2(out2_orig)
  );

  // Mapped design
  always_combinational_synthesis_verify_mapped dut_mapped(
    .a(a),
    .b(b),
    .c(c),
    .out1(out1_mapped),
    .out2(out2_mapped)
  );

  initial begin
    $display("========================================");
    $display("ModelSim Verification Testbench");
    $display("========================================");

    // Test 1
    $display("\nTest 1:");
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped)
    ) begin
      $display("  [PASS] Test 1 passed");
    end else begin
      $display("  [FAIL] Test 1 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
    end

    // Test 2
    $display("\nTest 2:");
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped)
    ) begin
      $display("  [PASS] Test 2 passed");
    end else begin
      $display("  [FAIL] Test 2 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
    end

    // Test 3
    $display("\nTest 3:");
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped)
    ) begin
      $display("  [PASS] Test 3 passed");
    end else begin
      $display("  [FAIL] Test 3 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
    end

    // Test 4
    $display("\nTest 4:");
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped)
    ) begin
      $display("  [PASS] Test 4 passed");
    end else begin
      $display("  [FAIL] Test 4 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
    end

    // Test 5
    $display("\nTest 5:");
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped)
    ) begin
      $display("  [PASS] Test 5 passed");
    end else begin
      $display("  [FAIL] Test 5 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
    end

    // Test 6
    $display("\nTest 6:");
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped)
    ) begin
      $display("  [PASS] Test 6 passed");
    end else begin
      $display("  [FAIL] Test 6 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
    end

    // Test 7
    $display("\nTest 7:");
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped)
    ) begin
      $display("  [PASS] Test 7 passed");
    end else begin
      $display("  [FAIL] Test 7 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
    end

    // Test 8
    $display("\nTest 8:");
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped)
    ) begin
      $display("  [PASS] Test 8 passed");
    end else begin
      $display("  [FAIL] Test 8 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
    end

    $display("\n========================================");
    $display("Simulation completed");
    $display("========================================");
    $finish;
  end

endmodule