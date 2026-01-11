// ============================================================
// CANNOT_DO Example 7: Physical Design Features
// ============================================================
// Đây là những gì MyLogic CHƯA làm được:
// - Place & Route (full P&R)
// - GDSII generation
// - Physical verification (DRC, LVS)
// - Timing closure
//
// Status: ❌ NOT SUPPORTED
// Reason: Cần PDK đầy đủ, tools chuyên dụng (Innovus, ICC)
// Current: Chỉ có basic placement/routing algorithms (educational)
// ============================================================

module physical_design(
    input a, b,
    output out
);

    // Logic synthesis OK
    assign out = a & b;
    
    // Nhưng CHƯA thể:
    // - Place cells trên chip
    // - Route wires giữa cells
    // - Generate GDSII files
    // - Physical verification
    // - Timing closure

endmodule

