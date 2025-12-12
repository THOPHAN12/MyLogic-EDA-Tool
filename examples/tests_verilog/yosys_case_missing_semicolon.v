// Derived from common syntax pitfalls, inspired by Yosys tests
module yosys_case_missing_semicolon(input a, input b, output y);
    // Missing semicolon after assign
    assign y = a & b
endmodule

