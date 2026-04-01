`timescale 1ns/1ps

module tb_01_combinational_gates_compare;

  reg a;
  reg b;
  reg c;
  reg d;

  wire ref_out_and;
  wire ref_out_or;
  wire ref_out_xor;
  wire ref_out_nand;
  wire ref_out_nor;
  wire ref_out_not;

  wire syn_out_and;
  wire syn_out_or;
  wire syn_out_xor;
  wire syn_out_nand;
  wire syn_out_nor;
  wire syn_out_not;

  wire opt_out_and;
  wire opt_out_or;
  wire opt_out_xor;
  wire opt_out_nand;
  wire opt_out_nor;
  wire opt_out_not;

  reg exp_out_and;
  reg exp_out_or;
  reg exp_out_xor;
  reg exp_out_nand;
  reg exp_out_nor;
  reg exp_out_not;

  integer i;
  integer errors;
  integer vector_errors;

  combinational_gates dut_ref (
    .a(a),
    .b(b),
    .c(c),
    .d(d),
    .out_and(ref_out_and),
    .out_or(ref_out_or),
    .out_xor(ref_out_xor),
    .out_nand(ref_out_nand),
    .out_nor(ref_out_nor),
    .out_not(ref_out_not)
  );

  combinational_gates_syn dut_syn (
    .a(a),
    .b(b),
    .c(c),
    .d(d),
    .out_and(syn_out_and),
    .out_or(syn_out_or),
    .out_xor(syn_out_xor),
    .out_nand(syn_out_nand),
    .out_nor(syn_out_nor),
    .out_not(syn_out_not)
  );

  combinational_gates_opt dut_opt (
    .a(a),
    .b(b),
    .c(c),
    .d(d),
    .out_and(opt_out_and),
    .out_or(opt_out_or),
    .out_xor(opt_out_xor),
    .out_nand(opt_out_nand),
    .out_nor(opt_out_nor),
    .out_not(opt_out_not)
  );

  task check_outputs;
    begin
      vector_errors = 0;
      exp_out_and  = a & b;
      exp_out_or   = a | b | c | d;
      exp_out_xor  = a ^ b;
      exp_out_nand = ~(a & b);
      exp_out_nor  = ~(a | b);
      exp_out_not  = ~a;

      if ({ref_out_and, ref_out_or, ref_out_xor, ref_out_nand, ref_out_nor, ref_out_not} !==
          {exp_out_and, exp_out_or, exp_out_xor, exp_out_nand, exp_out_nor, exp_out_not}) begin
        $display(
          "REF_MISMATCH a=%0d b=%0d c=%0d d=%0d | got=%b%b%b%b%b%b exp=%b%b%b%b%b%b",
          a, b, c, d,
          ref_out_and, ref_out_or, ref_out_xor, ref_out_nand, ref_out_nor, ref_out_not,
          exp_out_and, exp_out_or, exp_out_xor, exp_out_nand, exp_out_nor, exp_out_not
        );
        errors = errors + 1;
        vector_errors = vector_errors + 1;
      end

      if ({syn_out_and, syn_out_or, syn_out_xor, syn_out_nand, syn_out_nor, syn_out_not} !==
          {exp_out_and, exp_out_or, exp_out_xor, exp_out_nand, exp_out_nor, exp_out_not}) begin
        $display(
          "SYN_MISMATCH a=%0d b=%0d c=%0d d=%0d | got=%b%b%b%b%b%b exp=%b%b%b%b%b%b",
          a, b, c, d,
          syn_out_and, syn_out_or, syn_out_xor, syn_out_nand, syn_out_nor, syn_out_not,
          exp_out_and, exp_out_or, exp_out_xor, exp_out_nand, exp_out_nor, exp_out_not
        );
        errors = errors + 1;
        vector_errors = vector_errors + 1;
      end

      if ({opt_out_and, opt_out_or, opt_out_xor, opt_out_nand, opt_out_nor, opt_out_not} !==
          {exp_out_and, exp_out_or, exp_out_xor, exp_out_nand, exp_out_nor, exp_out_not}) begin
        $display(
          "OPT_MISMATCH a=%0d b=%0d c=%0d d=%0d | got=%b%b%b%b%b%b exp=%b%b%b%b%b%b",
          a, b, c, d,
          opt_out_and, opt_out_or, opt_out_xor, opt_out_nand, opt_out_nor, opt_out_not,
          exp_out_and, exp_out_or, exp_out_xor, exp_out_nand, exp_out_nor, exp_out_not
        );
        errors = errors + 1;
        vector_errors = vector_errors + 1;
      end

      if ({ref_out_and, ref_out_or, ref_out_xor, ref_out_nand, ref_out_nor, ref_out_not} !==
          {syn_out_and, syn_out_or, syn_out_xor, syn_out_nand, syn_out_nor, syn_out_not}) begin
        $display("REF_SYN_DIFF a=%0d b=%0d c=%0d d=%0d", a, b, c, d);
        errors = errors + 1;
        vector_errors = vector_errors + 1;
      end

      if ({ref_out_and, ref_out_or, ref_out_xor, ref_out_nand, ref_out_nor, ref_out_not} !==
          {opt_out_and, opt_out_or, opt_out_xor, opt_out_nand, opt_out_nor, opt_out_not}) begin
        $display("REF_OPT_DIFF a=%0d b=%0d c=%0d d=%0d", a, b, c, d);
        errors = errors + 1;
        vector_errors = vector_errors + 1;
      end

      if ({syn_out_and, syn_out_or, syn_out_xor, syn_out_nand, syn_out_nor, syn_out_not} !==
          {opt_out_and, opt_out_or, opt_out_xor, opt_out_nand, opt_out_nor, opt_out_not}) begin
        $display("SYN_OPT_DIFF a=%0d b=%0d c=%0d d=%0d", a, b, c, d);
        errors = errors + 1;
        vector_errors = vector_errors + 1;
      end

      if (vector_errors == 0) begin
        $display(
          "PASS a=%0d b=%0d c=%0d d=%0d | ref=%b%b%b%b%b%b syn=%b%b%b%b%b%b opt=%b%b%b%b%b%b",
          a, b, c, d,
          ref_out_and, ref_out_or, ref_out_xor, ref_out_nand, ref_out_nor, ref_out_not,
          syn_out_and, syn_out_or, syn_out_xor, syn_out_nand, syn_out_nor, syn_out_not,
          opt_out_and, opt_out_or, opt_out_xor, opt_out_nand, opt_out_nor, opt_out_not
        );
      end
    end
  endtask

  initial begin
    errors = 0;
    $display("=== Compare combinational_gates / syn / opt ===");

    for (i = 0; i < 16; i = i + 1) begin
      {a, b, c, d} = i[3:0];
      #1;
      check_outputs();
    end

    if (errors == 0) begin
      $display("RESULT PASS: reference, synthesized, and optimized all match on 16/16 vectors.");
    end else begin
      $display("RESULT FAIL: found %0d mismatches.", errors);
    end

    $finish;
  end

endmodule

