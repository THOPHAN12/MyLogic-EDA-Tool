module redundant_logic(a, b, c, out1, out2, out3);
  input a, b, c;
  output out1, out2, out3;
  
  // 1. Common Subexpression: a & b được tính 3 lần
  //    Parser sẽ tạo 3 nodes riêng biệt
  assign temp1 = a & b;
  assign temp2 = a & b;  // Duplicate của temp1
  assign temp3 = a & b;  // Duplicate của temp1
  
  // 2. Dead Code: temp_dead không được dùng trong outputs
  assign temp_dead = a | b | c;  // Không dùng -> DCE sẽ xóa
  
  // 3. Redundant Logic: temp6 và temp7 giống nhau
  assign temp6 = a ^ b;
  assign temp7 = a ^ b;  // Duplicate của temp6
  
  // 4. Unbalanced Logic: Chain dài (nhiều AND)
  assign chain1 = a & b & c;  // Có thể balance
  
  // Outputs - chỉ dùng một số intermediate signals
  assign out1 = temp1 | temp2;  // Dùng temp1, temp2 (duplicate)
  assign out2 = temp3 ^ temp6;  // Dùng temp3 (duplicate), temp6
  assign out3 = chain1;  // Dùng chain1
  // temp_dead KHÔNG được dùng -> Dead code
endmodule

