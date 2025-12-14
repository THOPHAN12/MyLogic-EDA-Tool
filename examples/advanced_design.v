/*
 * Advanced Design Example for MyLogic EDA Tool
 * 
 * This module demonstrates ALL features supported by the parser:
 * - Parameters and parameterized widths
 * - Signed/unsigned declarations
 * - Generate blocks (for/if)
 * - Case statements (case/casex/casez)
 * - Bit slices and replication
 * - Memory declarations and array indexing
 * - Functions and tasks
 * - Module instantiation (named/ordered ports)
 * - Always blocks (sequential and combinational)
 * - Arithmetic, bitwise, logical, comparison, shift operations
 */

module advanced_design #(
    parameter WIDTH = 8,
    parameter DEPTH = 16,
    parameter N = 4,
    parameter ENABLE_FEATURE = 1
)(
    // Input ports with signed/unsigned
    input signed [WIDTH-1:0] data_in,
    input unsigned [WIDTH-1:0] addr,
    input [N-1:0] control,
    input clk,
    input rst_n,
    input enable,
    
    // Output ports
    output reg signed [WIDTH*2-1:0] result,
    output [WIDTH-1:0] mem_out,
    output [WIDTH-1:0] processed_data,
    output [WIDTH-1:0] function_result
);

    // Internal signals
    wire signed [WIDTH-1:0] temp1, temp2;
    wire [WIDTH-1:0] temp3;
    wire [WIDTH-1:0] temp4;
    
    // Memory declaration
    reg [WIDTH-1:0] memory [0:DEPTH-1];
    reg [WIDTH-1:0] buffer [0:3];
    
    // Combinational always block
    always @(*) begin
        // Arithmetic operations
        temp1 = data_in + 8'd10;
        temp2 = data_in - 8'd5;
        
        // Bitwise operations
        temp3 = data_in & 8'hFF;
        temp4 = data_in | 8'hAA;
        
        // Logical operations
        if (data_in > 8'd100) begin
            processed_data = temp1;
        end else begin
            processed_data = temp2;
        end
    end
    
    // Sequential always block
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            result <= 0;
        end else if (enable) begin
            // Nonblocking assignment
            result <= {temp1, temp2};
        end
    end
    
    // Memory write (sequential)
    always @(posedge clk) begin
        if (enable) begin
            memory[addr] <= data_in;
        end
    end
    
    // Memory read (combinational)
    assign mem_out = memory[addr];
    
    // Generate block with for loop
    generate
        genvar i;
        for (i = 0; i < N; i = i + 1) begin : gen_buffer
            always @(posedge clk) begin
                if (rst_n) begin
                    buffer[i] <= data_in[i*2 +: 2];  // Bit slice
                end
            end
        end
    endgenerate
    
    // Generate block with if statement
    generate
        if (ENABLE_FEATURE == 1) begin : gen_feature
            wire [WIDTH-1:0] feature_out;
            assign feature_out = data_in ^ 8'h55;
        end
    endgenerate
    
    // Case statement
    reg [WIDTH-1:0] case_result;
    always @(*) begin
        case (control)
            2'b00: case_result = temp1;
            2'b01: case_result = temp2;
            2'b10: case_result = temp3;
            2'b11: case_result = temp4;
            default: case_result = 8'h00;
        endcase
    end
    
    // Casex statement
    reg [WIDTH-1:0] casex_result;
    always @(*) begin
        casex (control)
            2'b0x: casex_result = temp1;
            2'b1x: casex_result = temp2;
            default: casex_result = 8'h00;
        endcase
    end
    
    // Casez statement
    reg [WIDTH-1:0] casez_result;
    always @(*) begin
        casez (control)
            2'b0?: casez_result = temp1;
            2'b1?: casez_result = temp2;
            default: casez_result = 8'h00;
        endcase
    end
    
    // Bit manipulation examples
    wire [WIDTH-1:0] bit_slice = data_in[7:4];           // Bit slice
    wire single_bit = data_in[0];                        // Single bit
    wire [WIDTH*2-1:0] replicated = {4{data_in}};       // Replication
    wire [WIDTH*2-1:0] concatenated = {temp1, temp2};    // Concatenation
    wire [WIDTH*3-1:0] nested = {{2{data_in}}, temp1};   // Nested replication
    
    // Shift operations
    wire [WIDTH-1:0] left_shift = data_in << 2;
    wire [WIDTH-1:0] right_shift = data_in >> 2;
    wire [WIDTH-1:0] arithmetic_shift = data_in >>> 1;
    
    // Comparison operations
    wire gt = data_in > 8'd50;
    wire lt = data_in < 8'd100;
    wire eq = data_in == 8'd75;
    wire ne = data_in != 8'd0;
    
    // Function declaration
    function signed [WIDTH-1:0] add_with_offset;
        input signed [WIDTH-1:0] a, b;
        input [3:0] offset;
        begin
            add_with_offset = a + b + offset;
        end
    endfunction
    
    // Function call
    assign function_result = add_with_offset(data_in, 8'd10, 4'd5);
    
    // Task declaration
    task reset_memory;
        integer i;
        begin
            for (i = 0; i < DEPTH; i = i + 1) begin
                memory[i] = 0;
            end
        end
    endtask
    
    // Module instantiation with named ports
    simple_adder #(
        .WIDTH(WIDTH)
    ) adder_inst (
        .a(temp1),
        .b(temp2),
        .sum(concatenated[WIDTH-1:0])
    );
    
    // Module instantiation with ordered ports
    simple_multiplier mult_inst (
        temp1,
        temp2,
        concatenated[WIDTH*2-1:WIDTH]
    );
    
    // Complex expression with all operations
    wire [WIDTH-1:0] complex_expr;
    assign complex_expr = ((data_in + temp1) * (temp2 - 8'd5)) >> 2;
    
    // Ternary operator
    wire [WIDTH-1:0] ternary_result;
    assign ternary_result = (enable) ? temp1 : temp2;
    
    // Nested ternary
    wire [WIDTH-1:0] nested_ternary;
    assign nested_ternary = (control[0]) ? 
                            ((control[1]) ? temp1 : temp2) : 
                            ((control[1]) ? temp3 : temp4);
    
endmodule

// Simple adder module for instantiation
module simple_adder #(
    parameter WIDTH = 8
)(
    input [WIDTH-1:0] a,
    input [WIDTH-1:0] b,
    output [WIDTH:0] sum
);
    assign sum = a + b;
endmodule

// Simple multiplier module for instantiation
module simple_multiplier(
    input [7:0] a,
    input [7:0] b,
    output [15:0] product
);
    assign product = a * b;
endmodule

