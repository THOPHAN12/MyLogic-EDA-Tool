// Missing 'assign' keyword before assignment
module yosys_case_missing_assign(input a, input b, output y);
    // Should be "assign y = ..."
    y = a | b;
endmodule

