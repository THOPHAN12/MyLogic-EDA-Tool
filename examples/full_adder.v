module full_adder(a, b, cin, sum, cout);
  input a, b;
  input cin;
  output sum, cout;
  wire r;
  assign r=a;
  assign sum = r ^ cin ^ b;
  assign cout = (r & b) | (cin & (r ^ b));
endmodule