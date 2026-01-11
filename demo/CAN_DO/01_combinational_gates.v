// ============================================================
// CAN_DO Example 1: Combinational Logic Gates
// ============================================================
// Đây là những gì MyLogic đã làm được tốt:
// - Parse và synthesis các cổng combinational cơ bản
// - Hỗ trợ đầy đủ AND, OR, XOR, NAND, NOR, NOT
// - Synthesis thành AIG và optimization
//
// Status: ✅ FULLY SUPPORTED
// ============================================================

module combinational_gates(
    input a,
    input b,
    input c,
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
    assign out_or = a | b | c;
    
    // XOR gate
    assign out_xor = a ^ b;
    
    // NAND gate
    assign out_nand = ~(a & b);
    
    // NOR gate
    assign out_nor = ~(a | b);
    
    // NOT gate
    assign out_not = ~a;

endmodule

