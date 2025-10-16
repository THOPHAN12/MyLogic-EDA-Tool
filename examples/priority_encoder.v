module priority_encoder(in, out, valid);
  input [7:0] in;
  output [2:0] out;
  output valid;
  
  assign out = (in[7]) ? 3'b111 :
               (in[6]) ? 3'b110 :
               (in[5]) ? 3'b101 :
               (in[4]) ? 3'b100 :
               (in[3]) ? 3'b011 :
               (in[2]) ? 3'b010 :
               (in[1]) ? 3'b001 :
               3'b000;
  
  assign valid = (in != 8'b00000000) ? 1'b1 : 1'b0;
endmodule
