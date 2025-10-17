// Module hierarchy example: Large module calling small modules
// This demonstrates module instantiation capabilities

// Small module 1: Half Adder
module half_adder(a, b, sum, carry);
  input a, b;
  output sum, carry;
  
  assign sum = a ^ b;
  assign carry = a & b;
endmodule

// Small module 2: 2-to-1 Multiplexer
module mux2to1(sel, in0, in1, out);
  input sel, in0, in1;
  output out;
  
  assign out = sel ? in1 : in0;
endmodule

// Small module 3: 4-bit Adder
module adder4bit(a, b, cin, sum, cout);
  input [3:0] a, b;
  input cin;
  output [3:0] sum;
  output cout;
  
  wire [3:0] temp_carry;
  
  // Instantiate half adders for each bit
  half_adder ha0(a[0], b[0], sum[0], temp_carry[0]);
  half_adder ha1(a[1], b[1], sum[1], temp_carry[1]);
  half_adder ha2(a[2], b[2], sum[2], temp_carry[2]);
  half_adder ha3(a[3], b[3], sum[3], temp_carry[3]);
  
  // Generate carry chain
  assign cout = temp_carry[3] | (temp_carry[2] & temp_carry[1]) | (temp_carry[1] & temp_carry[0]);
endmodule

// Large module: Arithmetic Logic Unit (ALU)
module alu_unit(op, a, b, result, flags);
  input [1:0] op;        // Operation select
  input [3:0] a, b;      // 4-bit operands
  output [3:0] result;   // 4-bit result
  output [2:0] flags;    // Flags: [zero, carry, overflow]
  
  // Internal wires
  wire [3:0] add_result, sub_result, and_result, or_result;
  wire [3:0] mux_out;
  wire add_cout, sub_cout;
  
  // Instantiate 4-bit adder for addition
  adder4bit adder_inst(
    .a(a),
    .b(b), 
    .cin(1'b0),
    .sum(add_result),
    .cout(add_cout)
  );
  
  // Instantiate 4-bit adder for subtraction (using 2's complement)
  adder4bit sub_inst(
    .a(a),
    .b(~b + 1),  // 2's complement of b
    .cin(1'b0),
    .sum(sub_result),
    .cout(sub_cout)
  );
  
  // Bitwise operations
  assign and_result = a & b;
  assign or_result = a | b;
  
  // Result multiplexer - instantiate 4 muxes for 4-bit result
  mux2to1 mux0(op[0], and_result[0], or_result[0], mux_out[0]);
  mux2to1 mux1(op[0], and_result[1], or_result[1], mux_out[1]);
  mux2to1 mux2(op[0], and_result[2], or_result[2], mux_out[2]);
  mux2to1 mux3(op[0], and_result[3], or_result[3], mux_out[3]);
  
  // Final result multiplexer
  mux2to1 final_mux(op[1], mux_out[0], add_result[0], result[0]);
  mux2to1 final_mux1(op[1], mux_out[1], add_result[1], result[1]);
  mux2to1 final_mux2(op[1], mux_out[2], add_result[2], result[2]);
  mux2to1 final_mux3(op[1], mux_out[3], add_result[3], result[3]);
  
  // Flag generation
  assign flags[0] = (result == 4'b0000);  // Zero flag
  assign flags[1] = add_cout;             // Carry flag
  assign flags[2] = (a[3] == b[3]) && (a[3] != result[3]); // Overflow flag
endmodule

// Top-level module: Processor Unit
module processor_unit(clk, reset, opcode, data_a, data_b, result, status);
  input clk, reset;
  input [2:0] opcode;    // Extended operation code
  input [3:0] data_a, data_b;
  output [3:0] result;
  output [3:0] status;   // Extended status flags
  
  // Internal signals
  wire [1:0] alu_op;
  wire [2:0] alu_flags;
  wire [3:0] alu_result;
  
  // Operation decoder
  assign alu_op = opcode[1:0];
  
  // Instantiate ALU unit
  alu_unit alu_inst(
    .op(alu_op),
    .a(data_a),
    .b(data_b),
    .result(alu_result),
    .flags(alu_flags)
  );
  
  // Result and status assignment
  assign result = alu_result;
  assign status = {opcode[2], alu_flags}; // [extended, zero, carry, overflow]
endmodule
