/*
 * Comprehensive Test Module for MyLogic EDA Tool
 * 
 * This module tests all Verilog features supported by the parser:
 * - Parameters and parameterized widths
 * - Signed/unsigned declarations
 * - Generate blocks (for/if)
 * - Case statements (case/casex/casez)
 * - Bit slices and replication
 * - Memory declarations and array indexing
 * - Functions and tasks
 * - Module instantiations (named/ordered ports)
 * - Arithmetic, bitwise, and logical operations
 * - Always blocks (combinational and sequential)
 */

module comprehensive_test #(
    parameter WIDTH = 8,
    parameter DEPTH = 16,
    parameter N = 4
)(
    input signed [WIDTH-1:0] a,
    input signed [WIDTH-1:0] b,
    input [N-1:0] sel,
    input clk,
    input rst,
    output reg signed [WIDTH-1:0] result,
    output [WIDTH*2-1:0] product,
    output [WIDTH-1:0] mem_out
);

    // Local parameters
    localparam ADDR_WIDTH = 4;
    localparam MAX_VAL = WIDTH * 2;
    
    // Wires and regs with signed/unsigned
    wire signed [WIDTH-1:0] sum, diff;
    wire unsigned [WIDTH-1:0] and_result, or_result, xor_result;
    reg [WIDTH-1:0] mem [DEPTH-1:0];
    reg [ADDR_WIDTH-1:0] addr;
    wire [WIDTH-1:0] shifted_left, shifted_right;
    
    // Arithmetic operations
    assign sum = a + b;
    assign diff = a - b;
    assign product = a * b;
    
    // Bitwise operations
    assign and_result = a & b;
    assign or_result = a | b;
    assign xor_result = a ^ b;
    
    // Shift operations
    assign shifted_left = a << 1;
    assign shifted_right = a >> 1;
    
    // Bit slices with parameterized indices
    wire [3:0] upper_bits = a[WIDTH-1:WIDTH-4];
    wire [3:0] lower_bits = a[3:0];
    wire [1:0] middle_bits = a[5:4];
    
    // Replication
    wire [WIDTH-1:0] replicated = {N{a[3:0]}};
    wire [WIDTH*2-1:0] double_replicated = {2{a}};
    
    // Concatenation
    wire [WIDTH*2-1:0] concat = {a, b};
    wire [WIDTH*3-1:0] triple_concat = {a, b, sum};
    
    // Nested concatenation with replication
    wire [WIDTH*2-1:0] nested = {a, {4{b[1:0]}}};
    
    // Case statement
    always @(*) begin
        case (sel)
            4'b0000: result = sum;
            4'b0001: result = diff;
            4'b0010: result = and_result;
            4'b0011: result = or_result;
            4'b0100: result = xor_result;
            4'b0101: result = shifted_left;
            4'b0110: result = shifted_right;
            4'b0111: result = upper_bits;
            4'b1000: result = lower_bits;
            default: result = 8'b0;
        endcase
    end
    
    // Memory access with array indexing
    always @(posedge clk) begin
        if (rst) begin
            addr <= 0;
        end else begin
            addr <= addr + 1;
        end
    end
    
    assign mem_out = mem[addr];
    
    // Memory write
    always @(posedge clk) begin
        if (!rst) begin
            mem[addr] <= sum;
        end
    end
    
    // Generate block - for loop
    genvar i;
    generate
        for (i = 0; i < N; i = i + 1) begin : gen_loop
            wire [WIDTH-1:0] temp;
            assign temp = a + i;
        end
        
        // Generate block - if statement
        if (N > 2) begin
            wire [WIDTH-1:0] extra;
            assign extra = a + b;
        end
        
        if (WIDTH >= 8) begin
            wire [7:0] wide_signal;
            assign wide_signal = a[7:0];
        end
    endgenerate
    
    // Function with signed/unsigned
    function signed [WIDTH-1:0] add_with_offset;
        input signed [WIDTH-1:0] x, y;
        input [3:0] offset;
        begin
            add_with_offset = x + y + offset;
        end
    endfunction
    
    // Function with parameterized width
    function [WIDTH*2-1:0] multiply;
        input [WIDTH-1:0] x, y;
        begin
            multiply = x * y;
        end
    endfunction
    
    // Task
    task update_memory;
        input [ADDR_WIDTH-1:0] addr_in;
        input [WIDTH-1:0] data_in;
        begin
            mem[addr_in] = data_in;
        end
    endtask
    
    // Module instantiation with named ports
    wire [WIDTH-1:0] sub_result;
    submodule #(.WIDTH(WIDTH)) sub_inst (
        .a(a),
        .b(b),
        .out(sub_result)
    );
    
    // Module instantiation with ordered ports
    wire [WIDTH-1:0] add_result;
    adder_module add_inst (a, b, add_result);
    
    // Complex expression with ternary operator
    wire [WIDTH-1:0] ternary_result;
    assign ternary_result = (a > b) ? a : b;
    
    // Logical operations
    wire logical_and = (a > 0) && (b > 0);
    wire logical_or = (a == 0) || (b == 0);
    wire logical_not = !(a == b);
    
    // Reduction operations
    wire and_reduce = &a;
    wire or_reduce = |a;
    wire xor_reduce = ^a;
    
    // Comparison operations
    wire eq = (a == b);
    wire ne = (a != b);
    wire gt = (a > b);
    wire lt = (a < b);
    wire ge = (a >= b);
    wire le = (a <= b);
    
endmodule

// Submodule for instantiation test - named ports
module submodule #(parameter WIDTH = 8)(
    input [WIDTH-1:0] a,
    input [WIDTH-1:0] b,
    output [WIDTH-1:0] out
);
    assign out = a - b;
endmodule

// Submodule for instantiation test - ordered ports
module adder_module(
    input [7:0] a,
    input [7:0] b,
    output [7:0] sum
);
    assign sum = a + b;
endmodule


