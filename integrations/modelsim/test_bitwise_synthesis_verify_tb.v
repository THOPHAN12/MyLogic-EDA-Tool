`timescale 1ns/1ps

module test_bitwise_synthesis_verify_tb;

  reg a;
  reg b;

  wire and_result_orig;
  wire and_result_mapped;
  wire or_result_orig;
  wire or_result_mapped;
  wire xor_result_orig;
  wire xor_result_mapped;
  wire xnor_result_orig;
  wire xnor_result_mapped;
  wire not_a_orig;
  wire not_a_mapped;

  // Original design
  test_bitwise_synthesis_verify_original dut_original(
    .a(a),
    .b(b),
    .and_result(and_result_orig),
    .or_result(or_result_orig),
    .xor_result(xor_result_orig),
    .xnor_result(xnor_result_orig),
    .not_a(not_a_orig)
  );

  // Mapped design
  test_bitwise_synthesis_verify_mapped dut_mapped(
    .a(a),
    .b(b),
    .and_result(and_result_mapped),
    .or_result(or_result_mapped),
    .xor_result(xor_result_mapped),
    .xnor_result(xnor_result_mapped),
    .not_a(not_a_mapped)
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
    $display("  and_result_orig = %b, and_result_mapped = %b", and_result_orig, and_result_mapped);
    $display("  or_result_orig = %b, or_result_mapped = %b", or_result_orig, or_result_mapped);
    $display("  xor_result_orig = %b, xor_result_mapped = %b", xor_result_orig, xor_result_mapped);
    $display("  xnor_result_orig = %b, xnor_result_mapped = %b", xnor_result_orig, xnor_result_mapped);
    $display("  not_a_orig = %b, not_a_mapped = %b", not_a_orig, not_a_mapped);
    if (
(and_result_orig == and_result_mapped) && (or_result_orig == or_result_mapped) && (xor_result_orig == xor_result_mapped) && (xnor_result_orig == xnor_result_mapped) && (not_a_orig == not_a_mapped)
    ) begin
      $display("  [PASS] Test 1 passed");
    end else begin
      $display("  [FAIL] Test 1 failed - outputs don't match");
      if (and_result_orig != and_result_mapped)
        $display("    and_result: original=%b, mapped=%b", and_result_orig, and_result_mapped);
      if (or_result_orig != or_result_mapped)
        $display("    or_result: original=%b, mapped=%b", or_result_orig, or_result_mapped);
      if (xor_result_orig != xor_result_mapped)
        $display("    xor_result: original=%b, mapped=%b", xor_result_orig, xor_result_mapped);
      if (xnor_result_orig != xnor_result_mapped)
        $display("    xnor_result: original=%b, mapped=%b", xnor_result_orig, xnor_result_mapped);
      if (not_a_orig != not_a_mapped)
        $display("    not_a: original=%b, mapped=%b", not_a_orig, not_a_mapped);
    end

    // Test 2
    $display("\nTest 2:");
    a = 0;
    b = 1;
    #10;  // Wait for propagation
    $display("  and_result_orig = %b, and_result_mapped = %b", and_result_orig, and_result_mapped);
    $display("  or_result_orig = %b, or_result_mapped = %b", or_result_orig, or_result_mapped);
    $display("  xor_result_orig = %b, xor_result_mapped = %b", xor_result_orig, xor_result_mapped);
    $display("  xnor_result_orig = %b, xnor_result_mapped = %b", xnor_result_orig, xnor_result_mapped);
    $display("  not_a_orig = %b, not_a_mapped = %b", not_a_orig, not_a_mapped);
    if (
(and_result_orig == and_result_mapped) && (or_result_orig == or_result_mapped) && (xor_result_orig == xor_result_mapped) && (xnor_result_orig == xnor_result_mapped) && (not_a_orig == not_a_mapped)
    ) begin
      $display("  [PASS] Test 2 passed");
    end else begin
      $display("  [FAIL] Test 2 failed - outputs don't match");
      if (and_result_orig != and_result_mapped)
        $display("    and_result: original=%b, mapped=%b", and_result_orig, and_result_mapped);
      if (or_result_orig != or_result_mapped)
        $display("    or_result: original=%b, mapped=%b", or_result_orig, or_result_mapped);
      if (xor_result_orig != xor_result_mapped)
        $display("    xor_result: original=%b, mapped=%b", xor_result_orig, xor_result_mapped);
      if (xnor_result_orig != xnor_result_mapped)
        $display("    xnor_result: original=%b, mapped=%b", xnor_result_orig, xnor_result_mapped);
      if (not_a_orig != not_a_mapped)
        $display("    not_a: original=%b, mapped=%b", not_a_orig, not_a_mapped);
    end

    // Test 3
    $display("\nTest 3:");
    a = 1;
    b = 0;
    #10;  // Wait for propagation
    $display("  and_result_orig = %b, and_result_mapped = %b", and_result_orig, and_result_mapped);
    $display("  or_result_orig = %b, or_result_mapped = %b", or_result_orig, or_result_mapped);
    $display("  xor_result_orig = %b, xor_result_mapped = %b", xor_result_orig, xor_result_mapped);
    $display("  xnor_result_orig = %b, xnor_result_mapped = %b", xnor_result_orig, xnor_result_mapped);
    $display("  not_a_orig = %b, not_a_mapped = %b", not_a_orig, not_a_mapped);
    if (
(and_result_orig == and_result_mapped) && (or_result_orig == or_result_mapped) && (xor_result_orig == xor_result_mapped) && (xnor_result_orig == xnor_result_mapped) && (not_a_orig == not_a_mapped)
    ) begin
      $display("  [PASS] Test 3 passed");
    end else begin
      $display("  [FAIL] Test 3 failed - outputs don't match");
      if (and_result_orig != and_result_mapped)
        $display("    and_result: original=%b, mapped=%b", and_result_orig, and_result_mapped);
      if (or_result_orig != or_result_mapped)
        $display("    or_result: original=%b, mapped=%b", or_result_orig, or_result_mapped);
      if (xor_result_orig != xor_result_mapped)
        $display("    xor_result: original=%b, mapped=%b", xor_result_orig, xor_result_mapped);
      if (xnor_result_orig != xnor_result_mapped)
        $display("    xnor_result: original=%b, mapped=%b", xnor_result_orig, xnor_result_mapped);
      if (not_a_orig != not_a_mapped)
        $display("    not_a: original=%b, mapped=%b", not_a_orig, not_a_mapped);
    end

    // Test 4
    $display("\nTest 4:");
    a = 1;
    b = 1;
    #10;  // Wait for propagation
    $display("  and_result_orig = %b, and_result_mapped = %b", and_result_orig, and_result_mapped);
    $display("  or_result_orig = %b, or_result_mapped = %b", or_result_orig, or_result_mapped);
    $display("  xor_result_orig = %b, xor_result_mapped = %b", xor_result_orig, xor_result_mapped);
    $display("  xnor_result_orig = %b, xnor_result_mapped = %b", xnor_result_orig, xnor_result_mapped);
    $display("  not_a_orig = %b, not_a_mapped = %b", not_a_orig, not_a_mapped);
    if (
(and_result_orig == and_result_mapped) && (or_result_orig == or_result_mapped) && (xor_result_orig == xor_result_mapped) && (xnor_result_orig == xnor_result_mapped) && (not_a_orig == not_a_mapped)
    ) begin
      $display("  [PASS] Test 4 passed");
    end else begin
      $display("  [FAIL] Test 4 failed - outputs don't match");
      if (and_result_orig != and_result_mapped)
        $display("    and_result: original=%b, mapped=%b", and_result_orig, and_result_mapped);
      if (or_result_orig != or_result_mapped)
        $display("    or_result: original=%b, mapped=%b", or_result_orig, or_result_mapped);
      if (xor_result_orig != xor_result_mapped)
        $display("    xor_result: original=%b, mapped=%b", xor_result_orig, xor_result_mapped);
      if (xnor_result_orig != xnor_result_mapped)
        $display("    xnor_result: original=%b, mapped=%b", xnor_result_orig, xnor_result_mapped);
      if (not_a_orig != not_a_mapped)
        $display("    not_a: original=%b, mapped=%b", not_a_orig, not_a_mapped);
    end

    $display("\n========================================");
    $display("Simulation completed");
    $display("========================================");
    $finish;
  end

endmodule