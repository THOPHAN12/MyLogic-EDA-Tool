module combinational_gates(
    input a,
    input b,
    input c,
    input d,
    output out_and,
    output out_or,
    output out_xor,
    output out_nand,
    output out_nor,
    output out_not
);

    // AND gate
    assign out_and = a & b;
    
    // OR gate
    assign out_or = a | b | c | d;
    
    // XOR gate
    assign out_xor = a ^ b;
    // NAND gate
    assign out_nand = ~(a & b);
    
    // NOR gate
    assign out_nor = ~(a | b);
    
    // NOT gate
    assign out_not = ~a;

endmodule

