`timescale 1ns/1ps

module complex_expressions_synthesis_verify_tb;

  reg a;
  reg b;
  reg c;
  reg d;

  wire out1_orig;
  wire out1_mapped;
  wire out2_orig;
  wire out2_mapped;
  wire out3_orig;
  wire out3_mapped;

  // Original design
  complex_expressions_synthesis_verify_original dut_original(
    .a(a),
    .b(b),
    .c(c),
    .d(d),
    .out1(out1_orig),
    .out2(out2_orig),
    .out3(out3_orig)
  );

  // Mapped design
  complex_expressions_synthesis_verify_mapped dut_mapped(
    .a(a),
    .b(b),
    .c(c),
    .d(d),
    .out1(out1_mapped),
    .out2(out2_mapped),
    .out3(out3_mapped)
  );

  initial begin
    $display("========================================");
    $display("ModelSim Verification Testbench");
    $display("========================================");

    // Test 1
    $display("\nTest 1:");
    a = 0;
    b = 0;
    c = 0;
    d = 0;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 1 passed");
    end else begin
      $display("  [FAIL] Test 1 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 2
    $display("\nTest 2:");
    a = 0;
    b = 0;
    c = 0;
    d = 1;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 2 passed");
    end else begin
      $display("  [FAIL] Test 2 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 3
    $display("\nTest 3:");
    a = 0;
    b = 0;
    c = 1;
    d = 0;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 3 passed");
    end else begin
      $display("  [FAIL] Test 3 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 4
    $display("\nTest 4:");
    a = 0;
    b = 0;
    c = 1;
    d = 1;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 4 passed");
    end else begin
      $display("  [FAIL] Test 4 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 5
    $display("\nTest 5:");
    a = 0;
    b = 1;
    c = 0;
    d = 0;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 5 passed");
    end else begin
      $display("  [FAIL] Test 5 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 6
    $display("\nTest 6:");
    a = 0;
    b = 1;
    c = 0;
    d = 1;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 6 passed");
    end else begin
      $display("  [FAIL] Test 6 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 7
    $display("\nTest 7:");
    a = 0;
    b = 1;
    c = 1;
    d = 0;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 7 passed");
    end else begin
      $display("  [FAIL] Test 7 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 8
    $display("\nTest 8:");
    a = 0;
    b = 1;
    c = 1;
    d = 1;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 8 passed");
    end else begin
      $display("  [FAIL] Test 8 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 9
    $display("\nTest 9:");
    a = 1;
    b = 0;
    c = 0;
    d = 0;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 9 passed");
    end else begin
      $display("  [FAIL] Test 9 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 10
    $display("\nTest 10:");
    a = 1;
    b = 0;
    c = 0;
    d = 1;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 10 passed");
    end else begin
      $display("  [FAIL] Test 10 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 11
    $display("\nTest 11:");
    a = 1;
    b = 0;
    c = 1;
    d = 0;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 11 passed");
    end else begin
      $display("  [FAIL] Test 11 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 12
    $display("\nTest 12:");
    a = 1;
    b = 0;
    c = 1;
    d = 1;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 12 passed");
    end else begin
      $display("  [FAIL] Test 12 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 13
    $display("\nTest 13:");
    a = 1;
    b = 1;
    c = 0;
    d = 0;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 13 passed");
    end else begin
      $display("  [FAIL] Test 13 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 14
    $display("\nTest 14:");
    a = 1;
    b = 1;
    c = 0;
    d = 1;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 14 passed");
    end else begin
      $display("  [FAIL] Test 14 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 15
    $display("\nTest 15:");
    a = 1;
    b = 1;
    c = 1;
    d = 0;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 15 passed");
    end else begin
      $display("  [FAIL] Test 15 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    // Test 16
    $display("\nTest 16:");
    a = 1;
    b = 1;
    c = 1;
    d = 1;
    #10;  // Wait for propagation
    $display("  out1_orig = %b, out1_mapped = %b", out1_orig, out1_mapped);
    $display("  out2_orig = %b, out2_mapped = %b", out2_orig, out2_mapped);
    $display("  out3_orig = %b, out3_mapped = %b", out3_orig, out3_mapped);
    if (
(out1_orig == out1_mapped) && (out2_orig == out2_mapped) && (out3_orig == out3_mapped)
    ) begin
      $display("  [PASS] Test 16 passed");
    end else begin
      $display("  [FAIL] Test 16 failed - outputs don't match");
      if (out1_orig != out1_mapped)
        $display("    out1: original=%b, mapped=%b", out1_orig, out1_mapped);
      if (out2_orig != out2_mapped)
        $display("    out2: original=%b, mapped=%b", out2_orig, out2_mapped);
      if (out3_orig != out3_mapped)
        $display("    out3: original=%b, mapped=%b", out3_orig, out3_mapped);
    end

    $display("\n========================================");
    $display("Simulation completed");
    $display("========================================");
    $finish;
  end

endmodule