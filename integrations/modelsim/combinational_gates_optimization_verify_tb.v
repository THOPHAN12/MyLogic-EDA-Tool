`timescale 1ns/1ps

module combinational_gates_optimization_verify_tb;

  reg a;
  reg b;
  reg c;

  wire out_and_orig;
  wire out_and_mapped;
  wire out_or_orig;
  wire out_or_mapped;
  wire out_xor_orig;
  wire out_xor_mapped;
  wire out_nand_orig;
  wire out_nand_mapped;
  wire out_nor_orig;
  wire out_nor_mapped;
  wire out_not_orig;
  wire out_not_mapped;

  // Original design
  combinational_gates_optimization_verify_original dut_original(
    .a(a),
    .b(b),
    .c(c),
    .out_and(out_and_orig),
    .out_or(out_or_orig),
    .out_xor(out_xor_orig),
    .out_nand(out_nand_orig),
    .out_nor(out_nor_orig),
    .out_not(out_not_orig)
  );

  // Mapped design
  combinational_gates_optimization_verify_mapped dut_mapped(
    .a(a),
    .b(b),
    .c(c),
    .out_and(out_and_mapped),
    .out_or(out_or_mapped),
    .out_xor(out_xor_mapped),
    .out_nand(out_nand_mapped),
    .out_nor(out_nor_mapped),
    .out_not(out_not_mapped)
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
    #10;  // Wait for propagation
    $display("  out_and_orig = %b, out_and_mapped = %b", out_and_orig, out_and_mapped);
    $display("  out_or_orig = %b, out_or_mapped = %b", out_or_orig, out_or_mapped);
    $display("  out_xor_orig = %b, out_xor_mapped = %b", out_xor_orig, out_xor_mapped);
    $display("  out_nand_orig = %b, out_nand_mapped = %b", out_nand_orig, out_nand_mapped);
    $display("  out_nor_orig = %b, out_nor_mapped = %b", out_nor_orig, out_nor_mapped);
    $display("  out_not_orig = %b, out_not_mapped = %b", out_not_orig, out_not_mapped);
    if (
(out_and_orig == out_and_mapped) && (out_or_orig == out_or_mapped) && (out_xor_orig == out_xor_mapped) && (out_nand_orig == out_nand_mapped) && (out_nor_orig == out_nor_mapped) && (out_not_orig == out_not_mapped)
    ) begin
      $display("  [PASS] Test 1 passed");
    end else begin
      $display("  [FAIL] Test 1 failed - outputs don't match");
      if (out_and_orig != out_and_mapped)
        $display("    out_and: original=%b, mapped=%b", out_and_orig, out_and_mapped);
      if (out_or_orig != out_or_mapped)
        $display("    out_or: original=%b, mapped=%b", out_or_orig, out_or_mapped);
      if (out_xor_orig != out_xor_mapped)
        $display("    out_xor: original=%b, mapped=%b", out_xor_orig, out_xor_mapped);
      if (out_nand_orig != out_nand_mapped)
        $display("    out_nand: original=%b, mapped=%b", out_nand_orig, out_nand_mapped);
      if (out_nor_orig != out_nor_mapped)
        $display("    out_nor: original=%b, mapped=%b", out_nor_orig, out_nor_mapped);
      if (out_not_orig != out_not_mapped)
        $display("    out_not: original=%b, mapped=%b", out_not_orig, out_not_mapped);
    end

    // Test 2
    $display("\nTest 2:");
    a = 0;
    b = 0;
    c = 1;
    #10;  // Wait for propagation
    $display("  out_and_orig = %b, out_and_mapped = %b", out_and_orig, out_and_mapped);
    $display("  out_or_orig = %b, out_or_mapped = %b", out_or_orig, out_or_mapped);
    $display("  out_xor_orig = %b, out_xor_mapped = %b", out_xor_orig, out_xor_mapped);
    $display("  out_nand_orig = %b, out_nand_mapped = %b", out_nand_orig, out_nand_mapped);
    $display("  out_nor_orig = %b, out_nor_mapped = %b", out_nor_orig, out_nor_mapped);
    $display("  out_not_orig = %b, out_not_mapped = %b", out_not_orig, out_not_mapped);
    if (
(out_and_orig == out_and_mapped) && (out_or_orig == out_or_mapped) && (out_xor_orig == out_xor_mapped) && (out_nand_orig == out_nand_mapped) && (out_nor_orig == out_nor_mapped) && (out_not_orig == out_not_mapped)
    ) begin
      $display("  [PASS] Test 2 passed");
    end else begin
      $display("  [FAIL] Test 2 failed - outputs don't match");
      if (out_and_orig != out_and_mapped)
        $display("    out_and: original=%b, mapped=%b", out_and_orig, out_and_mapped);
      if (out_or_orig != out_or_mapped)
        $display("    out_or: original=%b, mapped=%b", out_or_orig, out_or_mapped);
      if (out_xor_orig != out_xor_mapped)
        $display("    out_xor: original=%b, mapped=%b", out_xor_orig, out_xor_mapped);
      if (out_nand_orig != out_nand_mapped)
        $display("    out_nand: original=%b, mapped=%b", out_nand_orig, out_nand_mapped);
      if (out_nor_orig != out_nor_mapped)
        $display("    out_nor: original=%b, mapped=%b", out_nor_orig, out_nor_mapped);
      if (out_not_orig != out_not_mapped)
        $display("    out_not: original=%b, mapped=%b", out_not_orig, out_not_mapped);
    end

    // Test 3
    $display("\nTest 3:");
    a = 0;
    b = 1;
    c = 0;
    #10;  // Wait for propagation
    $display("  out_and_orig = %b, out_and_mapped = %b", out_and_orig, out_and_mapped);
    $display("  out_or_orig = %b, out_or_mapped = %b", out_or_orig, out_or_mapped);
    $display("  out_xor_orig = %b, out_xor_mapped = %b", out_xor_orig, out_xor_mapped);
    $display("  out_nand_orig = %b, out_nand_mapped = %b", out_nand_orig, out_nand_mapped);
    $display("  out_nor_orig = %b, out_nor_mapped = %b", out_nor_orig, out_nor_mapped);
    $display("  out_not_orig = %b, out_not_mapped = %b", out_not_orig, out_not_mapped);
    if (
(out_and_orig == out_and_mapped) && (out_or_orig == out_or_mapped) && (out_xor_orig == out_xor_mapped) && (out_nand_orig == out_nand_mapped) && (out_nor_orig == out_nor_mapped) && (out_not_orig == out_not_mapped)
    ) begin
      $display("  [PASS] Test 3 passed");
    end else begin
      $display("  [FAIL] Test 3 failed - outputs don't match");
      if (out_and_orig != out_and_mapped)
        $display("    out_and: original=%b, mapped=%b", out_and_orig, out_and_mapped);
      if (out_or_orig != out_or_mapped)
        $display("    out_or: original=%b, mapped=%b", out_or_orig, out_or_mapped);
      if (out_xor_orig != out_xor_mapped)
        $display("    out_xor: original=%b, mapped=%b", out_xor_orig, out_xor_mapped);
      if (out_nand_orig != out_nand_mapped)
        $display("    out_nand: original=%b, mapped=%b", out_nand_orig, out_nand_mapped);
      if (out_nor_orig != out_nor_mapped)
        $display("    out_nor: original=%b, mapped=%b", out_nor_orig, out_nor_mapped);
      if (out_not_orig != out_not_mapped)
        $display("    out_not: original=%b, mapped=%b", out_not_orig, out_not_mapped);
    end

    // Test 4
    $display("\nTest 4:");
    a = 0;
    b = 1;
    c = 1;
    #10;  // Wait for propagation
    $display("  out_and_orig = %b, out_and_mapped = %b", out_and_orig, out_and_mapped);
    $display("  out_or_orig = %b, out_or_mapped = %b", out_or_orig, out_or_mapped);
    $display("  out_xor_orig = %b, out_xor_mapped = %b", out_xor_orig, out_xor_mapped);
    $display("  out_nand_orig = %b, out_nand_mapped = %b", out_nand_orig, out_nand_mapped);
    $display("  out_nor_orig = %b, out_nor_mapped = %b", out_nor_orig, out_nor_mapped);
    $display("  out_not_orig = %b, out_not_mapped = %b", out_not_orig, out_not_mapped);
    if (
(out_and_orig == out_and_mapped) && (out_or_orig == out_or_mapped) && (out_xor_orig == out_xor_mapped) && (out_nand_orig == out_nand_mapped) && (out_nor_orig == out_nor_mapped) && (out_not_orig == out_not_mapped)
    ) begin
      $display("  [PASS] Test 4 passed");
    end else begin
      $display("  [FAIL] Test 4 failed - outputs don't match");
      if (out_and_orig != out_and_mapped)
        $display("    out_and: original=%b, mapped=%b", out_and_orig, out_and_mapped);
      if (out_or_orig != out_or_mapped)
        $display("    out_or: original=%b, mapped=%b", out_or_orig, out_or_mapped);
      if (out_xor_orig != out_xor_mapped)
        $display("    out_xor: original=%b, mapped=%b", out_xor_orig, out_xor_mapped);
      if (out_nand_orig != out_nand_mapped)
        $display("    out_nand: original=%b, mapped=%b", out_nand_orig, out_nand_mapped);
      if (out_nor_orig != out_nor_mapped)
        $display("    out_nor: original=%b, mapped=%b", out_nor_orig, out_nor_mapped);
      if (out_not_orig != out_not_mapped)
        $display("    out_not: original=%b, mapped=%b", out_not_orig, out_not_mapped);
    end

    // Test 5
    $display("\nTest 5:");
    a = 1;
    b = 0;
    c = 0;
    #10;  // Wait for propagation
    $display("  out_and_orig = %b, out_and_mapped = %b", out_and_orig, out_and_mapped);
    $display("  out_or_orig = %b, out_or_mapped = %b", out_or_orig, out_or_mapped);
    $display("  out_xor_orig = %b, out_xor_mapped = %b", out_xor_orig, out_xor_mapped);
    $display("  out_nand_orig = %b, out_nand_mapped = %b", out_nand_orig, out_nand_mapped);
    $display("  out_nor_orig = %b, out_nor_mapped = %b", out_nor_orig, out_nor_mapped);
    $display("  out_not_orig = %b, out_not_mapped = %b", out_not_orig, out_not_mapped);
    if (
(out_and_orig == out_and_mapped) && (out_or_orig == out_or_mapped) && (out_xor_orig == out_xor_mapped) && (out_nand_orig == out_nand_mapped) && (out_nor_orig == out_nor_mapped) && (out_not_orig == out_not_mapped)
    ) begin
      $display("  [PASS] Test 5 passed");
    end else begin
      $display("  [FAIL] Test 5 failed - outputs don't match");
      if (out_and_orig != out_and_mapped)
        $display("    out_and: original=%b, mapped=%b", out_and_orig, out_and_mapped);
      if (out_or_orig != out_or_mapped)
        $display("    out_or: original=%b, mapped=%b", out_or_orig, out_or_mapped);
      if (out_xor_orig != out_xor_mapped)
        $display("    out_xor: original=%b, mapped=%b", out_xor_orig, out_xor_mapped);
      if (out_nand_orig != out_nand_mapped)
        $display("    out_nand: original=%b, mapped=%b", out_nand_orig, out_nand_mapped);
      if (out_nor_orig != out_nor_mapped)
        $display("    out_nor: original=%b, mapped=%b", out_nor_orig, out_nor_mapped);
      if (out_not_orig != out_not_mapped)
        $display("    out_not: original=%b, mapped=%b", out_not_orig, out_not_mapped);
    end

    // Test 6
    $display("\nTest 6:");
    a = 1;
    b = 0;
    c = 1;
    #10;  // Wait for propagation
    $display("  out_and_orig = %b, out_and_mapped = %b", out_and_orig, out_and_mapped);
    $display("  out_or_orig = %b, out_or_mapped = %b", out_or_orig, out_or_mapped);
    $display("  out_xor_orig = %b, out_xor_mapped = %b", out_xor_orig, out_xor_mapped);
    $display("  out_nand_orig = %b, out_nand_mapped = %b", out_nand_orig, out_nand_mapped);
    $display("  out_nor_orig = %b, out_nor_mapped = %b", out_nor_orig, out_nor_mapped);
    $display("  out_not_orig = %b, out_not_mapped = %b", out_not_orig, out_not_mapped);
    if (
(out_and_orig == out_and_mapped) && (out_or_orig == out_or_mapped) && (out_xor_orig == out_xor_mapped) && (out_nand_orig == out_nand_mapped) && (out_nor_orig == out_nor_mapped) && (out_not_orig == out_not_mapped)
    ) begin
      $display("  [PASS] Test 6 passed");
    end else begin
      $display("  [FAIL] Test 6 failed - outputs don't match");
      if (out_and_orig != out_and_mapped)
        $display("    out_and: original=%b, mapped=%b", out_and_orig, out_and_mapped);
      if (out_or_orig != out_or_mapped)
        $display("    out_or: original=%b, mapped=%b", out_or_orig, out_or_mapped);
      if (out_xor_orig != out_xor_mapped)
        $display("    out_xor: original=%b, mapped=%b", out_xor_orig, out_xor_mapped);
      if (out_nand_orig != out_nand_mapped)
        $display("    out_nand: original=%b, mapped=%b", out_nand_orig, out_nand_mapped);
      if (out_nor_orig != out_nor_mapped)
        $display("    out_nor: original=%b, mapped=%b", out_nor_orig, out_nor_mapped);
      if (out_not_orig != out_not_mapped)
        $display("    out_not: original=%b, mapped=%b", out_not_orig, out_not_mapped);
    end

    // Test 7
    $display("\nTest 7:");
    a = 1;
    b = 1;
    c = 0;
    #10;  // Wait for propagation
    $display("  out_and_orig = %b, out_and_mapped = %b", out_and_orig, out_and_mapped);
    $display("  out_or_orig = %b, out_or_mapped = %b", out_or_orig, out_or_mapped);
    $display("  out_xor_orig = %b, out_xor_mapped = %b", out_xor_orig, out_xor_mapped);
    $display("  out_nand_orig = %b, out_nand_mapped = %b", out_nand_orig, out_nand_mapped);
    $display("  out_nor_orig = %b, out_nor_mapped = %b", out_nor_orig, out_nor_mapped);
    $display("  out_not_orig = %b, out_not_mapped = %b", out_not_orig, out_not_mapped);
    if (
(out_and_orig == out_and_mapped) && (out_or_orig == out_or_mapped) && (out_xor_orig == out_xor_mapped) && (out_nand_orig == out_nand_mapped) && (out_nor_orig == out_nor_mapped) && (out_not_orig == out_not_mapped)
    ) begin
      $display("  [PASS] Test 7 passed");
    end else begin
      $display("  [FAIL] Test 7 failed - outputs don't match");
      if (out_and_orig != out_and_mapped)
        $display("    out_and: original=%b, mapped=%b", out_and_orig, out_and_mapped);
      if (out_or_orig != out_or_mapped)
        $display("    out_or: original=%b, mapped=%b", out_or_orig, out_or_mapped);
      if (out_xor_orig != out_xor_mapped)
        $display("    out_xor: original=%b, mapped=%b", out_xor_orig, out_xor_mapped);
      if (out_nand_orig != out_nand_mapped)
        $display("    out_nand: original=%b, mapped=%b", out_nand_orig, out_nand_mapped);
      if (out_nor_orig != out_nor_mapped)
        $display("    out_nor: original=%b, mapped=%b", out_nor_orig, out_nor_mapped);
      if (out_not_orig != out_not_mapped)
        $display("    out_not: original=%b, mapped=%b", out_not_orig, out_not_mapped);
    end

    // Test 8
    $display("\nTest 8:");
    a = 1;
    b = 1;
    c = 1;
    #10;  // Wait for propagation
    $display("  out_and_orig = %b, out_and_mapped = %b", out_and_orig, out_and_mapped);
    $display("  out_or_orig = %b, out_or_mapped = %b", out_or_orig, out_or_mapped);
    $display("  out_xor_orig = %b, out_xor_mapped = %b", out_xor_orig, out_xor_mapped);
    $display("  out_nand_orig = %b, out_nand_mapped = %b", out_nand_orig, out_nand_mapped);
    $display("  out_nor_orig = %b, out_nor_mapped = %b", out_nor_orig, out_nor_mapped);
    $display("  out_not_orig = %b, out_not_mapped = %b", out_not_orig, out_not_mapped);
    if (
(out_and_orig == out_and_mapped) && (out_or_orig == out_or_mapped) && (out_xor_orig == out_xor_mapped) && (out_nand_orig == out_nand_mapped) && (out_nor_orig == out_nor_mapped) && (out_not_orig == out_not_mapped)
    ) begin
      $display("  [PASS] Test 8 passed");
    end else begin
      $display("  [FAIL] Test 8 failed - outputs don't match");
      if (out_and_orig != out_and_mapped)
        $display("    out_and: original=%b, mapped=%b", out_and_orig, out_and_mapped);
      if (out_or_orig != out_or_mapped)
        $display("    out_or: original=%b, mapped=%b", out_or_orig, out_or_mapped);
      if (out_xor_orig != out_xor_mapped)
        $display("    out_xor: original=%b, mapped=%b", out_xor_orig, out_xor_mapped);
      if (out_nand_orig != out_nand_mapped)
        $display("    out_nand: original=%b, mapped=%b", out_nand_orig, out_nand_mapped);
      if (out_nor_orig != out_nor_mapped)
        $display("    out_nor: original=%b, mapped=%b", out_nor_orig, out_nor_mapped);
      if (out_not_orig != out_not_mapped)
        $display("    out_not: original=%b, mapped=%b", out_not_orig, out_not_mapped);
    end

    $display("\n========================================");
    $display("Simulation completed");
    $display("========================================");
    $finish;
  end

endmodule