/*
 * Standard Cell Library - Verilog Format
 * MyLogic EDA Tool Technology Libraries
 * 
 * Thư viện cell chuẩn cho technology mapping
 * Dựa trên các thư viện industry standard
 */

// Basic Gates - 2-input
module INV (input A, output Y);
    assign Y = ~A;
endmodule

module NAND2 (input A, B, output Y);
    assign Y = ~(A & B);
endmodule

module NOR2 (input A, B, output Y);
    assign Y = ~(A | B);
endmodule

module AND2 (input A, B, output Y);
    assign Y = A & B;
endmodule

module OR2 (input A, B, output Y);
    assign Y = A | B;
endmodule

module XOR2 (input A, B, output Y);
    assign Y = A ^ B;
endmodule

module XNOR2 (input A, B, output Y);
    assign Y = ~(A ^ B);
endmodule

// 3-input Gates
module NAND3 (input A, B, C, output Y);
    assign Y = ~(A & B & C);
endmodule

module NOR3 (input A, B, C, output Y);
    assign Y = ~(A | B | C);
endmodule

module AND3 (input A, B, C, output Y);
    assign Y = A & B & C;
endmodule

module OR3 (input A, B, C, output Y);
    assign Y = A | B | C;
endmodule

// Complex Gates
module AOI21 (input A, B, C, output Y);
    assign Y = ~((A & B) | C);
endmodule

module OAI21 (input A, B, C, output Y);
    assign Y = ~((A | B) & C);
endmodule

module AOI22 (input A, B, C, D, output Y);
    assign Y = ~((A & B) | (C & D));
endmodule

module OAI22 (input A, B, C, D, output Y);
    assign Y = ~((A | B) & (C | D));
endmodule

// 4-input Gates
module NAND4 (input A, B, C, D, output Y);
    assign Y = ~(A & B & C & D);
endmodule

module NOR4 (input A, B, C, D, output Y);
    assign Y = ~(A | B | C | D);
endmodule

module AND4 (input A, B, C, D, output Y);
    assign Y = A & B & C & D;
endmodule

module OR4 (input A, B, C, D, output Y);
    assign Y = A | B | C | D;
endmodule

// MUX Gates
module MUX2 (input A, B, S, output Y);
    assign Y = S ? B : A;
endmodule

module MUX4 (input A, B, C, D, input [1:0] S, output Y);
    assign Y = (S == 2'b00) ? A :
               (S == 2'b01) ? B :
               (S == 2'b10) ? C : D;
endmodule

// DFF - D Flip-Flop
module DFF (input D, CLK, RST, output reg Q);
    always @(posedge CLK or posedge RST) begin
        if (RST) Q <= 1'b0;
        else Q <= D;
    end
endmodule

// DFF with Enable
module DFFE (input D, CLK, RST, EN, output reg Q);
    always @(posedge CLK or posedge RST) begin
        if (RST) Q <= 1'b0;
        else if (EN) Q <= D;
    end
endmodule
