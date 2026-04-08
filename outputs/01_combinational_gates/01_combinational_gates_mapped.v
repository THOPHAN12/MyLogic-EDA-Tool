module 01_combinational_gates_mapped_mapped(
  input  wire a,
  input  wire b,
  input  wire c,
  input  wire d,
  output wire out_and,
  output wire out_or,
  output wire out_xor,
  output wire out_nand,
  output wire out_nor,
  output wire out_not
);

  wire CONST1;
  wire node_10;
  wire node_11;
  wire node_12;
  wire node_13;
  wire node_14;
  wire node_15;
  wire node_16;
  wire node_17;
  wire node_18;
  wire node_19;
  wire node_20;
  wire node_21;
  wire node_22;
  wire node_23;
  wire node_6;
  wire node_7;
  wire node_8;
  wire node_9;

  assign out_and = node_6;
  assign out_or = node_14;
  assign out_xor = node_20;
  assign out_nand = node_21;
  assign out_nor = node_23;
  assign out_not = node_9;

  sky130_fd_sc_hd__a21oi_1 u_node_6 (.A1(a), .A2(b), .Y(node_6));
  sky130_fd_sc_hd__clkinv_1 u_node_7 (.A(d), .Y(node_7));
  sky130_fd_sc_hd__clkinv_1 u_node_8 (.A(c), .Y(node_8));
  sky130_fd_sc_hd__clkinv_1 u_node_9 (.A(a), .Y(node_9));
  sky130_fd_sc_hd__clkinv_1 u_node_10 (.A(b), .Y(node_10));
  sky130_fd_sc_hd__a21oi_1 u_node_11 (.A1(node_9), .A2(node_10), .Y(node_11));
  sky130_fd_sc_hd__a21oi_1 u_node_12 (.A1(node_8), .A2(node_11), .Y(node_12));
  sky130_fd_sc_hd__a21oi_1 u_node_13 (.A1(node_7), .A2(node_12), .Y(node_13));
  sky130_fd_sc_hd__clkinv_1 u_node_14 (.A(node_13), .Y(node_14));
  sky130_fd_sc_hd__a21oi_1 u_node_15 (.A1(b), .A2(node_9), .Y(node_15));
  sky130_fd_sc_hd__clkinv_1 u_node_16 (.A(node_15), .Y(node_16));
  sky130_fd_sc_hd__a21oi_1 u_node_17 (.A1(a), .A2(node_10), .Y(node_17));
  sky130_fd_sc_hd__clkinv_1 u_node_18 (.A(node_17), .Y(node_18));
  sky130_fd_sc_hd__a21oi_1 u_node_19 (.A1(node_16), .A2(node_18), .Y(node_19));
  sky130_fd_sc_hd__clkinv_1 u_node_20 (.A(node_19), .Y(node_20));
  sky130_fd_sc_hd__clkinv_1 u_node_21 (.A(node_6), .Y(node_21));
  sky130_fd_sc_hd__clkinv_1 u_node_22 (.A(node_11), .Y(node_22));
  sky130_fd_sc_hd__clkinv_1 u_node_23 (.A(node_22), .Y(node_23));
endmodule
