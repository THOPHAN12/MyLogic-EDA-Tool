`timescale 1ns/1ps

module test_arithmetic_optimization_verify_tb;

  reg a;
  reg b;

  wire sum_orig;
  wire sum_mapped;
  wire diff_orig;
  wire diff_mapped;
  wire prod_orig;
  wire prod_mapped;
  wire quot_orig;
  wire quot_mapped;
  wire mod_orig;
  wire mod_mapped;

  // Original design
  test_arithmetic_optimization_verify_original dut_original(
    .a(a),
    .b(b),
    .sum(sum_orig),
    .diff(diff_orig),
    .prod(prod_orig),
    .quot(quot_orig),
    .mod(mod_orig)
  );

  // Mapped design
  test_arithmetic_optimization_verify_mapped dut_mapped(
    .a(a),
    .b(b),
    .sum(sum_mapped),
    .diff(diff_mapped),
    .prod(prod_mapped),
    .quot(quot_mapped),
    .mod(mod_mapped)
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
    $display("  sum_orig = %b, sum_mapped = %b", sum_orig, sum_mapped);
    $display("  diff_orig = %b, diff_mapped = %b", diff_orig, diff_mapped);
    $display("  prod_orig = %b, prod_mapped = %b", prod_orig, prod_mapped);
    $display("  quot_orig = %b, quot_mapped = %b", quot_orig, quot_mapped);
    $display("  mod_orig = %b, mod_mapped = %b", mod_orig, mod_mapped);
    if (
(sum_orig == sum_mapped) && (diff_orig == diff_mapped) && (prod_orig == prod_mapped) && (quot_orig == quot_mapped) && (mod_orig == mod_mapped)
    ) begin
      $display("  [PASS] Test 1 passed");
    end else begin
      $display("  [FAIL] Test 1 failed - outputs don't match");
      if (sum_orig != sum_mapped)
        $display("    sum: original=%b, mapped=%b", sum_orig, sum_mapped);
      if (diff_orig != diff_mapped)
        $display("    diff: original=%b, mapped=%b", diff_orig, diff_mapped);
      if (prod_orig != prod_mapped)
        $display("    prod: original=%b, mapped=%b", prod_orig, prod_mapped);
      if (quot_orig != quot_mapped)
        $display("    quot: original=%b, mapped=%b", quot_orig, quot_mapped);
      if (mod_orig != mod_mapped)
        $display("    mod: original=%b, mapped=%b", mod_orig, mod_mapped);
    end

    // Test 2
    $display("\nTest 2:");
    a = 0;
    b = 1;
    #10;  // Wait for propagation
    $display("  sum_orig = %b, sum_mapped = %b", sum_orig, sum_mapped);
    $display("  diff_orig = %b, diff_mapped = %b", diff_orig, diff_mapped);
    $display("  prod_orig = %b, prod_mapped = %b", prod_orig, prod_mapped);
    $display("  quot_orig = %b, quot_mapped = %b", quot_orig, quot_mapped);
    $display("  mod_orig = %b, mod_mapped = %b", mod_orig, mod_mapped);
    if (
(sum_orig == sum_mapped) && (diff_orig == diff_mapped) && (prod_orig == prod_mapped) && (quot_orig == quot_mapped) && (mod_orig == mod_mapped)
    ) begin
      $display("  [PASS] Test 2 passed");
    end else begin
      $display("  [FAIL] Test 2 failed - outputs don't match");
      if (sum_orig != sum_mapped)
        $display("    sum: original=%b, mapped=%b", sum_orig, sum_mapped);
      if (diff_orig != diff_mapped)
        $display("    diff: original=%b, mapped=%b", diff_orig, diff_mapped);
      if (prod_orig != prod_mapped)
        $display("    prod: original=%b, mapped=%b", prod_orig, prod_mapped);
      if (quot_orig != quot_mapped)
        $display("    quot: original=%b, mapped=%b", quot_orig, quot_mapped);
      if (mod_orig != mod_mapped)
        $display("    mod: original=%b, mapped=%b", mod_orig, mod_mapped);
    end

    // Test 3
    $display("\nTest 3:");
    a = 1;
    b = 0;
    #10;  // Wait for propagation
    $display("  sum_orig = %b, sum_mapped = %b", sum_orig, sum_mapped);
    $display("  diff_orig = %b, diff_mapped = %b", diff_orig, diff_mapped);
    $display("  prod_orig = %b, prod_mapped = %b", prod_orig, prod_mapped);
    $display("  quot_orig = %b, quot_mapped = %b", quot_orig, quot_mapped);
    $display("  mod_orig = %b, mod_mapped = %b", mod_orig, mod_mapped);
    if (
(sum_orig == sum_mapped) && (diff_orig == diff_mapped) && (prod_orig == prod_mapped) && (quot_orig == quot_mapped) && (mod_orig == mod_mapped)
    ) begin
      $display("  [PASS] Test 3 passed");
    end else begin
      $display("  [FAIL] Test 3 failed - outputs don't match");
      if (sum_orig != sum_mapped)
        $display("    sum: original=%b, mapped=%b", sum_orig, sum_mapped);
      if (diff_orig != diff_mapped)
        $display("    diff: original=%b, mapped=%b", diff_orig, diff_mapped);
      if (prod_orig != prod_mapped)
        $display("    prod: original=%b, mapped=%b", prod_orig, prod_mapped);
      if (quot_orig != quot_mapped)
        $display("    quot: original=%b, mapped=%b", quot_orig, quot_mapped);
      if (mod_orig != mod_mapped)
        $display("    mod: original=%b, mapped=%b", mod_orig, mod_mapped);
    end

    // Test 4
    $display("\nTest 4:");
    a = 1;
    b = 1;
    #10;  // Wait for propagation
    $display("  sum_orig = %b, sum_mapped = %b", sum_orig, sum_mapped);
    $display("  diff_orig = %b, diff_mapped = %b", diff_orig, diff_mapped);
    $display("  prod_orig = %b, prod_mapped = %b", prod_orig, prod_mapped);
    $display("  quot_orig = %b, quot_mapped = %b", quot_orig, quot_mapped);
    $display("  mod_orig = %b, mod_mapped = %b", mod_orig, mod_mapped);
    if (
(sum_orig == sum_mapped) && (diff_orig == diff_mapped) && (prod_orig == prod_mapped) && (quot_orig == quot_mapped) && (mod_orig == mod_mapped)
    ) begin
      $display("  [PASS] Test 4 passed");
    end else begin
      $display("  [FAIL] Test 4 failed - outputs don't match");
      if (sum_orig != sum_mapped)
        $display("    sum: original=%b, mapped=%b", sum_orig, sum_mapped);
      if (diff_orig != diff_mapped)
        $display("    diff: original=%b, mapped=%b", diff_orig, diff_mapped);
      if (prod_orig != prod_mapped)
        $display("    prod: original=%b, mapped=%b", prod_orig, prod_mapped);
      if (quot_orig != quot_mapped)
        $display("    quot: original=%b, mapped=%b", quot_orig, quot_mapped);
      if (mod_orig != mod_mapped)
        $display("    mod: original=%b, mapped=%b", mod_orig, mod_mapped);
    end

    $display("\n========================================");
    $display("Simulation completed");
    $display("========================================");
    $finish;
  end

endmodule