`timescale 1ns/1ps

module full_feature_test_synthesis_verify_tb;

  reg data_in;
  reg addr;
  reg control;
  reg signed;
  reg unsigned;
  reg clk;
  reg rst_n;
  reg enable;
  reg a;
  reg b;

  wire result_orig;
  wire result_mapped;
  wire mem_out_orig;
  wire mem_out_mapped;
  wire processed_data_orig;
  wire processed_data_mapped;

  // Original design
  full_feature_test_synthesis_verify_original dut_original(
    .data_in(data_in),
    .addr(addr),
    .control(control),
    .signed(signed),
    .unsigned(unsigned),
    .clk(clk),
    .rst_n(rst_n),
    .enable(enable),
    .a(a),
    .b(b),
    .result(result_orig),
    .mem_out(mem_out_orig),
    .processed_data(processed_data_orig)
  );

  // Mapped design
  full_feature_test_synthesis_verify_mapped dut_mapped(
    .data_in(data_in),
    .addr(addr),
    .control(control),
    .signed(signed),
    .unsigned(unsigned),
    .clk(clk),
    .rst_n(rst_n),
    .enable(enable),
    .a(a),
    .b(b),
    .result(result_mapped),
    .mem_out(mem_out_mapped),
    .processed_data(processed_data_mapped)
  );

  initial begin
    $display("========================================");
    $display("ModelSim Verification Testbench");
    $display("========================================");

    // Test 1
    $display("\nTest 1:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 0;
    enable = 0;
    a = 0;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 1 passed");
    end else begin
      $display("  [FAIL] Test 1 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 2
    $display("\nTest 2:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 0;
    enable = 0;
    a = 0;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 2 passed");
    end else begin
      $display("  [FAIL] Test 2 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 3
    $display("\nTest 3:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 0;
    enable = 0;
    a = 1;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 3 passed");
    end else begin
      $display("  [FAIL] Test 3 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 4
    $display("\nTest 4:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 0;
    enable = 0;
    a = 1;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 4 passed");
    end else begin
      $display("  [FAIL] Test 4 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 5
    $display("\nTest 5:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 0;
    enable = 1;
    a = 0;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 5 passed");
    end else begin
      $display("  [FAIL] Test 5 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 6
    $display("\nTest 6:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 0;
    enable = 1;
    a = 0;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 6 passed");
    end else begin
      $display("  [FAIL] Test 6 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 7
    $display("\nTest 7:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 0;
    enable = 1;
    a = 1;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 7 passed");
    end else begin
      $display("  [FAIL] Test 7 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 8
    $display("\nTest 8:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 0;
    enable = 1;
    a = 1;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 8 passed");
    end else begin
      $display("  [FAIL] Test 8 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 9
    $display("\nTest 9:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 1;
    enable = 0;
    a = 0;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 9 passed");
    end else begin
      $display("  [FAIL] Test 9 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 10
    $display("\nTest 10:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 1;
    enable = 0;
    a = 0;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 10 passed");
    end else begin
      $display("  [FAIL] Test 10 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 11
    $display("\nTest 11:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 1;
    enable = 0;
    a = 1;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 11 passed");
    end else begin
      $display("  [FAIL] Test 11 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 12
    $display("\nTest 12:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 1;
    enable = 0;
    a = 1;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 12 passed");
    end else begin
      $display("  [FAIL] Test 12 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 13
    $display("\nTest 13:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 1;
    enable = 1;
    a = 0;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 13 passed");
    end else begin
      $display("  [FAIL] Test 13 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 14
    $display("\nTest 14:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 1;
    enable = 1;
    a = 0;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 14 passed");
    end else begin
      $display("  [FAIL] Test 14 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 15
    $display("\nTest 15:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 1;
    enable = 1;
    a = 1;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 15 passed");
    end else begin
      $display("  [FAIL] Test 15 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 16
    $display("\nTest 16:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 0;
    rst_n = 1;
    enable = 1;
    a = 1;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 16 passed");
    end else begin
      $display("  [FAIL] Test 16 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 17
    $display("\nTest 17:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 0;
    enable = 0;
    a = 0;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 17 passed");
    end else begin
      $display("  [FAIL] Test 17 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 18
    $display("\nTest 18:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 0;
    enable = 0;
    a = 0;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 18 passed");
    end else begin
      $display("  [FAIL] Test 18 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 19
    $display("\nTest 19:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 0;
    enable = 0;
    a = 1;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 19 passed");
    end else begin
      $display("  [FAIL] Test 19 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 20
    $display("\nTest 20:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 0;
    enable = 0;
    a = 1;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 20 passed");
    end else begin
      $display("  [FAIL] Test 20 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 21
    $display("\nTest 21:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 0;
    enable = 1;
    a = 0;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 21 passed");
    end else begin
      $display("  [FAIL] Test 21 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 22
    $display("\nTest 22:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 0;
    enable = 1;
    a = 0;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 22 passed");
    end else begin
      $display("  [FAIL] Test 22 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 23
    $display("\nTest 23:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 0;
    enable = 1;
    a = 1;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 23 passed");
    end else begin
      $display("  [FAIL] Test 23 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 24
    $display("\nTest 24:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 0;
    enable = 1;
    a = 1;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 24 passed");
    end else begin
      $display("  [FAIL] Test 24 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 25
    $display("\nTest 25:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 1;
    enable = 0;
    a = 0;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 25 passed");
    end else begin
      $display("  [FAIL] Test 25 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 26
    $display("\nTest 26:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 1;
    enable = 0;
    a = 0;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 26 passed");
    end else begin
      $display("  [FAIL] Test 26 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 27
    $display("\nTest 27:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 1;
    enable = 0;
    a = 1;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 27 passed");
    end else begin
      $display("  [FAIL] Test 27 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 28
    $display("\nTest 28:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 1;
    enable = 0;
    a = 1;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 28 passed");
    end else begin
      $display("  [FAIL] Test 28 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 29
    $display("\nTest 29:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 1;
    enable = 1;
    a = 0;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 29 passed");
    end else begin
      $display("  [FAIL] Test 29 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 30
    $display("\nTest 30:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 1;
    enable = 1;
    a = 0;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 30 passed");
    end else begin
      $display("  [FAIL] Test 30 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 31
    $display("\nTest 31:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 1;
    enable = 1;
    a = 1;
    b = 0;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 31 passed");
    end else begin
      $display("  [FAIL] Test 31 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    // Test 32
    $display("\nTest 32:");
    data_in = 0;
    addr = 0;
    control = 0;
    signed = 0;
    unsigned = 0;
    clk = 1;
    rst_n = 1;
    enable = 1;
    a = 1;
    b = 1;
    #10;  // Wait for propagation
    $display("  result_orig = %b, result_mapped = %b", result_orig, result_mapped);
    $display("  mem_out_orig = %b, mem_out_mapped = %b", mem_out_orig, mem_out_mapped);
    $display("  processed_data_orig = %b, processed_data_mapped = %b", processed_data_orig, processed_data_mapped);
    if (
(result_orig == result_mapped) && (mem_out_orig == mem_out_mapped) && (processed_data_orig == processed_data_mapped)
    ) begin
      $display("  [PASS] Test 32 passed");
    end else begin
      $display("  [FAIL] Test 32 failed - outputs don't match");
      if (result_orig != result_mapped)
        $display("    result: original=%b, mapped=%b", result_orig, result_mapped);
      if (mem_out_orig != mem_out_mapped)
        $display("    mem_out: original=%b, mapped=%b", mem_out_orig, mem_out_mapped);
      if (processed_data_orig != processed_data_mapped)
        $display("    processed_data: original=%b, mapped=%b", processed_data_orig, processed_data_mapped);
    end

    $display("\n========================================");
    $display("Simulation completed");
    $display("========================================");
    $finish;
  end

endmodule