/*
 * Module Instantiation Examples
 * MyLogic EDA Tool - Module Hierarchy Support
 * 
 * Ví dụ về module lớn gọi module nhỏ
 */

// ============================================================================
// 1. BASIC MODULES (Sub-modules)
// ============================================================================

// Half Adder Module
module half_adder(
    input a, b,
    output sum, cout
);
    assign sum = a ^ b;
    assign cout = a & b;
endmodule

// Full Adder Module
module full_adder(
    input a, b, cin,
    output sum, cout
);
    wire s1, c1, c2;
    
    // Instantiate half adders
    half_adder ha1 (.a(a), .b(b), .sum(s1), .cout(c1));
    half_adder ha2 (.a(s1), .b(cin), .sum(sum), .cout(c2));
    
    assign cout = c1 | c2;
endmodule

// 2-to-1 Multiplexer Module
module mux2to1(
    input [3:0] a, b,
    input sel,
    output [3:0] out
);
    assign out = sel ? b : a;
endmodule

// 4-to-1 Multiplexer Module
module mux4to1(
    input [3:0] a, b, c, d,
    input [1:0] sel,
    output [3:0] out
);
    assign out = (sel == 2'b00) ? a :
                 (sel == 2'b01) ? b :
                 (sel == 2'b10) ? c :
                 d;
endmodule

// Arithmetic Logic Unit (ALU) Module
module alu(
    input [3:0] a, b,
    input [2:0] op,
    output [3:0] result,
    output zero, overflow
);
    wire [3:0] add_result, sub_result, and_result, or_result;
    
    assign add_result = a + b;
    assign sub_result = a - b;
    assign and_result = a & b;
    assign or_result = a | b;
    
    assign result = (op == 3'b000) ? add_result :
                    (op == 3'b001) ? sub_result :
                    (op == 3'b010) ? and_result :
                    (op == 3'b011) ? or_result :
                    (op == 3'b100) ? a ^ b :
                    (op == 3'b101) ? ~a :
                    (op == 3'b110) ? a << 1 :
                    a >> 1;
    
    assign zero = (result == 4'b0000);
    assign overflow = (op == 3'b000) ? (a[3] & b[3] & ~result[3]) | (~a[3] & ~b[3] & result[3]) :
                      (op == 3'b001) ? (a[3] & ~b[3] & ~result[3]) | (~a[3] & b[3] & result[3]) :
                      1'b0;
endmodule

// ============================================================================
// 2. COMPLEX MODULE WITH INSTANTIATIONS
// ============================================================================

module complex_processor(
    input [3:0] data_a, data_b,
    input [1:0] mux_sel,
    input [2:0] alu_op,
    input enable,
    output [3:0] final_result,
    output [3:0] mux_out,
    output [3:0] alu_out,
    output zero_flag,
    output overflow_flag,
    output valid
);
    
    // Internal wires
    wire [3:0] mux_result;
    wire [3:0] alu_result;
    wire alu_zero, alu_overflow;
    
    // Instantiate 4-to-1 MUX
    mux4to1 mux_inst (
        .a(data_a),
        .b(data_b),
        .c(4'b0000),
        .d(4'b1111),
        .sel(mux_sel),
        .out(mux_result)
    );
    
    // Instantiate ALU
    alu alu_inst (
        .a(mux_result),
        .b(data_b),
        .op(alu_op),
        .result(alu_result),
        .zero(alu_zero),
        .overflow(alu_overflow)
    );
    
    // Output assignments
    assign mux_out = mux_result;
    assign alu_out = alu_result;
    assign final_result = enable ? alu_result : 4'b0000;
    assign zero_flag = alu_zero;
    assign overflow_flag = alu_overflow;
    assign valid = enable;
endmodule

// ============================================================================
// 3. RIPPLE CARRY ADDER WITH MODULE INSTANTIATIONS
// ============================================================================

module ripple_carry_adder(
    input [3:0] a, b,
    input cin,
    output [3:0] sum,
    output cout
);
    wire c1, c2, c3;
    
    // Instantiate full adders
    full_adder fa0 (.a(a[0]), .b(b[0]), .cin(cin), .sum(sum[0]), .cout(c1));
    full_adder fa1 (.a(a[1]), .b(b[1]), .cin(c1), .sum(sum[1]), .cout(c2));
    full_adder fa2 (.a(a[2]), .b(b[2]), .cin(c2), .sum(sum[2]), .cout(c3));
    full_adder fa3 (.a(a[3]), .b(b[3]), .cin(c3), .sum(sum[3]), .cout(cout));
endmodule

// ============================================================================
// 4. DECODER WITH MODULE INSTANTIATIONS
// ============================================================================

// 2-to-4 Decoder Module
module decoder2to4(
    input [1:0] sel,
    input enable,
    output [3:0] out
);
    assign out[0] = enable & (sel == 2'b00);
    assign out[1] = enable & (sel == 2'b01);
    assign out[2] = enable & (sel == 2'b10);
    assign out[3] = enable & (sel == 2'b11);
endmodule

// 3-to-8 Decoder using 2-to-4 decoders
module decoder3to8(
    input [2:0] sel,
    input enable,
    output [7:0] out
);
    wire [3:0] decoder1_out, decoder2_out;
    
    // Instantiate 2-to-4 decoders
    decoder2to4 dec1 (
        .sel(sel[1:0]),
        .enable(enable & ~sel[2]),
        .out(decoder1_out)
    );
    
    decoder2to4 dec2 (
        .sel(sel[1:0]),
        .enable(enable & sel[2]),
        .out(decoder2_out)
    );
    
    // Combine outputs
    assign out[3:0] = decoder1_out;
    assign out[7:4] = decoder2_out;
endmodule

// ============================================================================
// 5. COMPARATOR WITH MODULE INSTANTIATIONS
// ============================================================================

// 1-bit Comparator Module
module comparator1bit(
    input a, b,
    output equal, greater, less
);
    assign equal = (a == b);
    assign greater = (a > b);
    assign less = (a < b);
endmodule

// 4-bit Comparator using 1-bit comparators
module comparator4bit(
    input [3:0] a, b,
    output equal, greater, less
);
    wire [3:0] eq, gt, lt;
    wire eq_all, gt_any, lt_any;
    
    // Instantiate 1-bit comparators
    comparator1bit comp0 (.a(a[0]), .b(b[0]), .equal(eq[0]), .greater(gt[0]), .less(lt[0]));
    comparator1bit comp1 (.a(a[1]), .b(b[1]), .equal(eq[1]), .greater(gt[1]), .less(lt[1]));
    comparator1bit comp2 (.a(a[2]), .b(b[2]), .equal(eq[2]), .greater(gt[2]), .less(lt[2]));
    comparator1bit comp3 (.a(a[3]), .b(b[3]), .equal(eq[3]), .greater(gt[3]), .less(lt[3]));
    
    // Combine results
    assign eq_all = &eq;
    assign gt_any = gt[3] | (eq[3] & gt[2]) | (eq[3] & eq[2] & gt[1]) | (eq[3] & eq[2] & eq[1] & gt[0]);
    assign lt_any = lt[3] | (eq[3] & lt[2]) | (eq[3] & eq[2] & lt[1]) | (eq[3] & eq[2] & eq[1] & lt[0]);
    
    assign equal = eq_all;
    assign greater = gt_any;
    assign less = lt_any;
endmodule

// ============================================================================
// 6. MAIN MODULE WITH ALL INSTANTIATIONS
// ============================================================================

module main_processor(
    input [3:0] operand_a, operand_b,
    input [1:0] mux_select,
    input [2:0] alu_operation,
    input [2:0] decoder_select,
    input processor_enable,
    output [3:0] processor_result,
    output [3:0] mux_output,
    output [3:0] alu_output,
    output [7:0] decoder_output,
    output zero_flag,
    output overflow_flag,
    output equal_flag,
    output greater_flag,
    output less_flag,
    output processor_valid
);
    
    // Internal wires
    wire [3:0] mux_to_alu;
    wire [3:0] alu_result;
    wire alu_zero, alu_overflow;
    wire comp_equal, comp_greater, comp_less;
    
    // Instantiate complex processor
    complex_processor proc_inst (
        .data_a(operand_a),
        .data_b(operand_b),
        .mux_sel(mux_select),
        .alu_op(alu_operation),
        .enable(processor_enable),
        .final_result(processor_result),
        .mux_out(mux_output),
        .alu_out(alu_output),
        .zero_flag(zero_flag),
        .overflow_flag(overflow_flag),
        .valid(processor_valid)
    );
    
    // Instantiate 3-to-8 decoder
    decoder3to8 decoder_inst (
        .sel(decoder_select),
        .enable(processor_enable),
        .out(decoder_output)
    );
    
    // Instantiate 4-bit comparator
    comparator4bit comparator_inst (
        .a(operand_a),
        .b(operand_b),
        .equal(equal_flag),
        .greater(greater_flag),
        .less(less_flag)
    );
    
    // Instantiate ripple carry adder
    ripple_carry_adder adder_inst (
        .a(operand_a),
        .b(operand_b),
        .cin(1'b0),
        .sum(),  // Not connected
        .cout()  // Not connected
    );
endmodule

/*
 * MODULE INSTANTIATION SYNTAX SUMMARY:
 * 
 * 1. Named port connections (recommended):
 *    module_name instance_name (
 *        .port_name(signal_name),
 *        .port_name(signal_name)
 *    );
 * 
 * 2. Positional port connections:
 *    module_name instance_name (signal1, signal2, signal3);
 * 
 * 3. Mixed connections:
 *    module_name instance_name (
 *        .port_name(signal_name),
 *        signal_name,  // positional
 *        .port_name(signal_name)
 *    );
 * 
 * 4. Bit range connections:
 *    module_name instance_name (
 *        .port_name(signal_name[3:0]),
 *        .port_name(signal_name[7:4])
 *    );
 * 
 * 5. Constant connections:
 *    module_name instance_name (
 *        .port_name(4'b0000),
 *        .port_name(1'b1)
 *    );
 * 
 * 6. Unconnected ports:
 *    module_name instance_name (
 *        .port_name(signal_name),
 *        .unused_port()  // Not connected
 *    );
 * 
 * All syntax supported by MyLogic EDA Tool!
 */
