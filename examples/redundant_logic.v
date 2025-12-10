module redundant_logic(a, b, c, out1, out2, out3);
  input a, b, c;
  output out1, out2, out3;
  
  // ============================================================
  // TEST CASE 1: COMMON SUBEXPRESSION ELIMINATION (CSE)
  // ============================================================
  // Thuật toán: Common Subexpression Elimination (CSE)
  // Mục đích: Phát hiện và loại bỏ các biểu thức con trùng lặp
  // Test: Expression "a & b" xuất hiện 3 lần trong circuit
  //       Parser sẽ tạo 3 nodes riêng biệt: and_0, and_1, and_2
  // Kết quả mong đợi: Strash sẽ phát hiện và merge thành 1 node duy nhất
  assign temp1 = a & b;  // Node: and_0 (AND với inputs: a, b)
  assign temp2 = a & b;  // Node: and_1 (Duplicate → Strash sẽ xóa)
  assign temp3 = a & b;  // Node: and_2 (Duplicate → Strash sẽ xóa)
  
  // ============================================================
  // TEST CASE 2: DEAD CODE ELIMINATION (DCE)
  // ============================================================
  // Thuật toán: Dead Code Elimination (DCE)
  // Mục đích: Loại bỏ các node không thể tiếp cận từ bất kỳ output nào
  // Test: temp_dead được tính nhưng KHÔNG được sử dụng trong bất kỳ output nào
  // Kết quả mong đợi: DCE sẽ phát hiện và xóa node or_3 (temp_dead)
  //                    Vì không có output nào sử dụng temp_dead
  assign temp_dead = a | b | c;  // Node: or_3 (DEAD CODE → DCE sẽ xóa)
  
  // ============================================================
  // TEST CASE 3: STRUCTURAL HASHING (STRASH)
  // ============================================================
  // Thuật toán: Structural Hashing (Strash)
  // Mục đích: Loại bỏ các node trùng lặp bằng cách hash structure
  // Test: Expression "a ^ b" xuất hiện 2 lần
  // Kết quả mong đợi: Strash sẽ phát hiện và merge temp6 và temp7 thành 1 node
  assign temp6 = a ^ b;  // Node: xor_4 (XOR với inputs: a, b)
  assign temp7 = a ^ b;  // Node: xor_5 (Duplicate → Strash sẽ xóa)
  
  // ============================================================
  // TEST CASE 4: LOGIC BALANCING (BALANCE)
  // ============================================================
  // Thuật toán: Logic Balancing (Balance)
  // Mục đích: Cân bằng độ sâu logic để tối ưu timing và critical path
  // Test: Chain dài với 3 inputs (a & b & c)
  //       Parser sẽ tạo 1 AND node với 3 inputs
  // Kết quả mong đợi: Balance sẽ cân bằng thành balanced tree structure
  //                   (nếu cần thiết cho timing optimization)
  assign chain1 = a & b & c;  // Node: and_6 (AND với 3 inputs: a, b, c)
                               //        → Balance có thể tạo balanced tree
  
  // ============================================================
  // OUTPUTS - Sử dụng các intermediate signals
  // ============================================================
  // Output 1: Sử dụng temp1 và temp2 (cả 2 đều là a & b sau Strash)
  //           → OR của cùng 1 signal có thể được simplify
  assign out1 = temp1 | temp2;  // Node: or_7 (OR: temp1 | temp2)
                                 //       Sau Strash: temp1=temp2=and_0
                                 //       → out1 = and_0 | and_0 = and_0 (có thể simplify)
  
  // Output 2: Sử dụng temp3 (a & b) và temp6 (a ^ b)
  //           → XOR của 2 biểu thức khác nhau
  assign out2 = temp3 ^ temp6;  // Node: xor_8 (XOR: temp3 ^ temp6)
                                 //       Sau Strash: temp3=and_0, temp6=xor_4
  
  // Output 3: Sử dụng chain1 (a & b & c)
  //           → Direct connection đến and_6
  assign out3 = chain1;  // Node: buf_9 → Sau Strash: direct to and_6
                          //      (BUF sẽ được xóa bởi Strash)
  
  // ============================================================
  // TÓM TẮT CÁC THUẬT TOÁN ĐƯỢC TEST:
  // ============================================================
  // 1. STRASH: Phát hiện và xóa duplicate nodes (and_1, and_2, xor_5, buf_9)
  // 2. DCE: Xóa dead code (or_3 = temp_dead)
  // 3. CSE: Không có gì để làm (Strash đã xử lý duplicates)
  // 4. CONSTPROP: Không có constants để propagate
  // 5. BALANCE: Cân bằng logic depth (chain1 = a & b & c)
  //
  // KẾT QUẢ MONG ĐỢI:
  // - Initial nodes: 10
  // - After Strash: 6 nodes (xóa 4 duplicates)
  // - After DCE: 5 nodes (xóa 1 dead code)
  // - Final: 5 nodes (and_0, xor_4, and_6, or_7, xor_8)
endmodule

