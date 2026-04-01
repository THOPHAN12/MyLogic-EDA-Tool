`timescale 1ns/1ps

module tb_02_complex_expressions;

  reg a;
  reg b;
  reg c;
  reg d;

  wire ref_out1;
  wire ref_out2;
  wire ref_out3;

  wire syn_out1;
  wire syn_out2;
  wire syn_out3;

  wire opt_out1;
  wire opt_out2;
  wire opt_out3;

  reg exp_out1;
  reg exp_out2;
  reg exp_out3;

  integer i;
  integer errors;
  integer vector_errors;

  complex_expressions dut_ref (
    .a(a),
    .b(b),
    .c(c),
    .d(d),
    .out1(ref_out1),
    .out2(ref_out2),
    .out3(ref_out3)
  );

  complex_expressions_syn dut_syn (
    .a(a),
    .b(b),
    .c(c),
    .d(d),
    .out1(syn_out1),
    .out2(syn_out2),
    .out3(syn_out3)
  );

  complex_expressions_opt dut_opt (
    .a(a),
    .b(b),
    .c(c),
    .d(d),
    .out1(opt_out1),
    .out2(opt_out2),
    .out3(opt_out3)
  );

  task check_outputs;
    begin
      vector_errors = 0;
      exp_out1 = (a & b) | (c & d);
      exp_out2 = (a & b & c) | d;
      exp_out3 = ~(a & b);

      if ({ref_out1, ref_out2, ref_out3} !== {exp_out1, exp_out2, exp_out3}) begin
        $display(
          "REF_MISMATCH a=%0d b=%0d c=%0d d=%0d | got=%b%b%b exp=%b%b%b",
          a, b, c, d,
          ref_out1, ref_out2, ref_out3,
          exp_out1, exp_out2, exp_out3
        );
        errors = errors + 1;
        vector_errors = vector_errors + 1;
      end

      if ({syn_out1, syn_out2, syn_out3} !== {exp_out1, exp_out2, exp_out3}) begin
        $display(
          "SYN_MISMATCH a=%0d b=%0d c=%0d d=%0d | got=%b%b%b exp=%b%b%b",
          a, b, c, d,
          syn_out1, syn_out2, syn_out3,
          exp_out1, exp_out2, exp_out3
        );
        errors = errors + 1;
        vector_errors = vector_errors + 1;
      end

      if ({opt_out1, opt_out2, opt_out3} !== {exp_out1, exp_out2, exp_out3}) begin
        $display(
          "OPT_MISMATCH a=%0d b=%0d c=%0d d=%0d | got=%b%b%b exp=%b%b%b",
          a, b, c, d,
          opt_out1, opt_out2, opt_out3,
          exp_out1, exp_out2, exp_out3
        );
        errors = errors + 1;
        vector_errors = vector_errors + 1;
      end

      if ({ref_out1, ref_out2, ref_out3} !== {syn_out1, syn_out2, syn_out3}) begin
        $display("REF_SYN_DIFF a=%0d b=%0d c=%0d d=%0d", a, b, c, d);
        errors = errors + 1;
        vector_errors = vector_errors + 1;
      end

      if ({ref_out1, ref_out2, ref_out3} !== {opt_out1, opt_out2, opt_out3}) begin
        $display("REF_OPT_DIFF a=%0d b=%0d c=%0d d=%0d", a, b, c, d);
        errors = errors + 1;
        vector_errors = vector_errors + 1;
      end

      if ({syn_out1, syn_out2, syn_out3} !== {opt_out1, opt_out2, opt_out3}) begin
        $display("SYN_OPT_DIFF a=%0d b=%0d c=%0d d=%0d", a, b, c, d);
        errors = errors + 1;
        vector_errors = vector_errors + 1;
      end

      if (vector_errors == 0) begin
        $display(
          "PASS a=%0d b=%0d c=%0d d=%0d | ref=%b%b%b syn=%b%b%b opt=%b%b%b",
          a, b, c, d,
          ref_out1, ref_out2, ref_out3,
          syn_out1, syn_out2, syn_out3,
          opt_out1, opt_out2, opt_out3
        );
      end
    end
  endtask

  initial begin
    errors = 0;
    $display("=== Compare complex_expressions / syn / opt ===");

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
