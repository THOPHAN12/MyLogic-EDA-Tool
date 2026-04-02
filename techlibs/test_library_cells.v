module INV_A1(input A, output Y);
  assign Y = ~A;
endmodule

module BUF_A1(input A, output Y);
  assign Y = A;
endmodule

module AND2_SMALL(input A, input B, output Y);
  assign Y = A & B;
endmodule

module AND2_FAST(input A, input B, output Y);
  assign Y = A & B;
endmodule

module OR2_SMALL(input A, input B, output Y);
  assign Y = A | B;
endmodule

module OR2_FAST(input A, input B, output Y);
  assign Y = A | B;
endmodule

module XOR2_REF(input A, input B, output Y);
  assign Y = A ^ B;
endmodule

module NAND2_REF(input A, input B, output Y);
  assign Y = ~(A & B);
endmodule

module NOR2_REF(input A, input B, output Y);
  assign Y = ~(A | B);
endmodule
