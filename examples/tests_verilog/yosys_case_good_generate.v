// Valid generate with for loop
module yosys_case_good_generate #(parameter N = 2) (input [N-1:0] a, output [N-1:0] y);
    genvar i;
    generate
        for (i = 0; i < N; i = i + 1) begin : genblk
            assign y[i] = a[i];
        end
    endgenerate
endmodule


