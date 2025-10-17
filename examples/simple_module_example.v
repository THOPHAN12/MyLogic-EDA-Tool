// Simple module hierarchy example

// Small module: Half Adder
module half_adder(a, b, sum, carry);
  input a, b;
  output sum, carry;
  
  assign sum = a ^ b;
  assign carry = a & b;
endmodule

// Top module: Full Adder using Half Adders
module full_adder(a, b, cin, sum, cout);
  input a, b, cin;
  output sum, cout;
  
  // Internal wires
  wire temp_sum, temp_carry1, temp_carry2;
  
  // Instantiate half adders
  half_adder ha1(a, b, temp_sum, temp_carry1);
  half_adder ha2(temp_sum, cin, sum, temp_carry2);
  
  // Generate final carry
  assign cout = temp_carry1 | temp_carry2;
endmodule
