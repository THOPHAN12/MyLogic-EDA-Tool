/*
 * Full Feature Test Module for MyLogic EDA Tool
 * 
 * This module demonstrates ALL features in a single module:
 * - Parameters and parameterized widths
 * - Signed/unsigned declarations
 * - Generate blocks (for/if)
 * - Case statements (case/casex/casez)
 * - Bit slices and replication
 * - Memory declarations and array indexing
 * - Functions and tasks
 * - Always blocks (sequential and combinational)
 * - All operations (arithmetic, bitwise, logical, comparison, shift)
 */

module full_feature_test #(
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
    output [WIDTH-1:0] function_result,
    output [WIDTH-1:0] case_result,
    output [WIDTH-1:0] bit_manip_result
);

    // Local parameters
    localparam ADDR_WIDTH = 4;
    localparam MAX_VAL = WIDTH * 2;
    
    // Internal signals
    wire signed [WIDTH-1:0] temp1, temp2;
    wire [WIDTH-1:0] temp3, temp4;
    wire [WIDTH-1:0] sum, diff, prod;
    wire [WIDTH-1:0] and_result, or_result, xor_result;
    wire [WIDTH-1:0] shifted_left, shifted_right, arithmetic_shift;
    
    // Memory declaration
    reg [WIDTH-1:0] memory [0:DEPTH-1];
    reg [WIDTH-1:0] buffer [0:3];
    
    // Combinational always block
    always @(*) begin
        // Arithmetic operations
        temp1 = data_in + 8'd10;
        temp2 = data_in - 8'd5;
        sum = temp1 + temp2;
        diff = temp1 - temp2;
        prod = temp1 * temp2;
        
        // Bitwise operations
        temp3 = data_in & 8'hFF;
        temp4 = data_in | 8'hAA;
        and_result = temp1 & temp2;
        or_result = temp1 | temp2;
        xor_result = temp1 ^ temp2;
        
        // Shift operations
        shifted_left = data_in << 2;
        shifted_right = data_in >> 2;
        arithmetic_shift = data_in >>> 1;
        
        // Comparison operations
        if (data_in > 8'd100) begin
            processed_data = temp1;
        end else if (data_in < 8'd50) begin
            processed_data = temp2;
        end else begin
            processed_data = temp3;
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
    reg [WIDTH-1:0] case_reg;
    always @(*) begin
        case (control)
            2'b00: case_reg = temp1;
            2'b01: case_reg = temp2;
            2'b10: case_reg = temp3;
            2'b11: case_reg = temp4;
            default: case_reg = 8'h00;
        endcase
    end
    assign case_result = case_reg;
    
    // Casex statement
    reg [WIDTH-1:0] casex_reg;
    always @(*) begin
        casex (control)
            2'b0x: casex_reg = temp1;
            2'b1x: casex_reg = temp2;
            default: casex_reg = 8'h00;
        endcase
    end
    
    // Casez statement
    reg [WIDTH-1:0] casez_reg;
    always @(*) begin
        casez (control)
            2'b0?: casez_reg = temp1;
            2'b1?: casez_reg = temp2;
            default: casez_reg = 8'h00;
        endcase
    end
    
    // Bit manipulation examples
    wire [WIDTH-1:0] bit_slice = data_in[7:4];           // Bit slice
    wire single_bit = data_in[0];                        // Single bit
    wire [WIDTH*2-1:0] replicated = {4{data_in}};       // Replication
    wire [WIDTH*2-1:0] concatenated = {temp1, temp2};    // Concatenation
    wire [WIDTH*3-1:0] nested = {{2{data_in}}, temp1};   // Nested replication
    
    assign bit_manip_result = concatenated[WIDTH-1:0];
    
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
    
    // Logical operations
    wire logical_and = (data_in > 8'd50) && (data_in < 8'd100);
    wire logical_or = (data_in == 8'd0) || (data_in == 8'd255);
    wire logical_not = !enable;
    
    // Comparison operations
    wire gt = data_in > 8'd50;
    wire lt = data_in < 8'd100;
    wire eq = data_in == 8'd75;
    wire ne = data_in != 8'd0;
    wire ge = data_in >= 8'd50;
    wire le = data_in <= 8'd100;
    
endmodule

