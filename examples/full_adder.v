module full_adder(a, b, cin, sum, cout);
  input a, b;
  input cin;
  output sum, cout;
  
  assign sum = a ^ b ^ cin;
  assign cout = (a & b) | (cin & (a ^ b));
endmodule
