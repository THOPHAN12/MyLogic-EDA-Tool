// Generate if example: keep one branch
module yosys_case_generate_if #(parameter USE_XOR = 1) (input a, input b, output y);
    generate
        if (USE_XOR)
            assign y = a ^ b;
        else
            assign y = a & b;
    endgenerate
endmodule


