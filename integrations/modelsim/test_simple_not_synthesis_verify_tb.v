`timescale 1ns/1ps

module test_simple_not_synthesis_verify_tb;

  reg a;
  reg b;

  wire not_a_orig;
  wire not_a_mapped;
  wire not_b_orig;
  wire not_b_mapped;

  // Original design
  test_simple_not_synthesis_verify_original dut_original(
    .a(a),
    .b(b),
    .not_a(not_a_orig),
    .not_b(not_b_orig)
  );

  // Mapped design
  test_simple_not_synthesis_verify_mapped dut_mapped(
    .a(a),
    .b(b),
    .not_a(not_a_mapped),
    .not_b(not_b_mapped)
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
    $display("  not_a_orig = %b, not_a_mapped = %b", not_a_orig, not_a_mapped);
    $display("  not_b_orig = %b, not_b_mapped = %b", not_b_orig, not_b_mapped);
    if (
(not_a_orig == not_a_mapped) && (not_b_orig == not_b_mapped)
    ) begin
      $display("  [PASS] Test 1 passed");
    end else begin
      $display("  [FAIL] Test 1 failed - outputs don't match");
      if (not_a_orig != not_a_mapped)
        $display("    not_a: original=%b, mapped=%b", not_a_orig, not_a_mapped);
      if (not_b_orig != not_b_mapped)
        $display("    not_b: original=%b, mapped=%b", not_b_orig, not_b_mapped);
    end

    // Test 2
    $display("\nTest 2:");
    a = 0;
    b = 1;
    #10;  // Wait for propagation
    $display("  not_a_orig = %b, not_a_mapped = %b", not_a_orig, not_a_mapped);
    $display("  not_b_orig = %b, not_b_mapped = %b", not_b_orig, not_b_mapped);
    if (
(not_a_orig == not_a_mapped) && (not_b_orig == not_b_mapped)
    ) begin
      $display("  [PASS] Test 2 passed");
    end else begin
      $display("  [FAIL] Test 2 failed - outputs don't match");
      if (not_a_orig != not_a_mapped)
        $display("    not_a: original=%b, mapped=%b", not_a_orig, not_a_mapped);
      if (not_b_orig != not_b_mapped)
        $display("    not_b: original=%b, mapped=%b", not_b_orig, not_b_mapped);
    end

    // Test 3
    $display("\nTest 3:");
    a = 1;
    b = 0;
    #10;  // Wait for propagation
    $display("  not_a_orig = %b, not_a_mapped = %b", not_a_orig, not_a_mapped);
    $display("  not_b_orig = %b, not_b_mapped = %b", not_b_orig, not_b_mapped);
    if (
(not_a_orig == not_a_mapped) && (not_b_orig == not_b_mapped)
    ) begin
      $display("  [PASS] Test 3 passed");
    end else begin
      $display("  [FAIL] Test 3 failed - outputs don't match");
      if (not_a_orig != not_a_mapped)
        $display("    not_a: original=%b, mapped=%b", not_a_orig, not_a_mapped);
      if (not_b_orig != not_b_mapped)
        $display("    not_b: original=%b, mapped=%b", not_b_orig, not_b_mapped);
    end

    // Test 4
    $display("\nTest 4:");
    a = 1;
    b = 1;
    #10;  // Wait for propagation
    $display("  not_a_orig = %b, not_a_mapped = %b", not_a_orig, not_a_mapped);
    $display("  not_b_orig = %b, not_b_mapped = %b", not_b_orig, not_b_mapped);
    if (
(not_a_orig == not_a_mapped) && (not_b_orig == not_b_mapped)
    ) begin
      $display("  [PASS] Test 4 passed");
    end else begin
      $display("  [FAIL] Test 4 failed - outputs don't match");
      if (not_a_orig != not_a_mapped)
        $display("    not_a: original=%b, mapped=%b", not_a_orig, not_a_mapped);
      if (not_b_orig != not_b_mapped)
        $display("    not_b: original=%b, mapped=%b", not_b_orig, not_b_mapped);
    end

    $display("\n========================================");
    $display("Simulation completed");
    $display("========================================");
    $finish;
  end

endmodule