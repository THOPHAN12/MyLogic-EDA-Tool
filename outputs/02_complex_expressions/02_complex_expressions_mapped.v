module 02_complex_expressions_mapped_mapped(
  input  wire a,
  input  wire b,
  input  wire c,
  input  wire d,
  output wire out1,
  output wire out2,
  output wire out3
);

  wire CONST1;
  wire node_10;
  wire node_11;
  wire node_12;
  wire node_13;
  wire node_14;
  wire node_15;
  wire node_16;
  wire node_6;
  wire node_7;
  wire node_8;
  wire node_9;

  assign out1 = node_11;
  assign out2 = node_16;
  assign out3 = node_7;

  sky130_fd_sc_hd__a21oi_1 u_node_6 (.A1(a), .A2(b), .Y(node_6));
  sky130_fd_sc_hd__clkinv_1 u_node_7 (.A(node_6), .Y(node_7));
  sky130_fd_sc_hd__a21oi_1 u_node_8 (.A1(c), .A2(d), .Y(node_8));
  sky130_fd_sc_hd__clkinv_1 u_node_9 (.A(node_8), .Y(node_9));
  sky130_fd_sc_hd__a21oi_1 u_node_10 (.A1(node_7), .A2(node_9), .Y(node_10));
  sky130_fd_sc_hd__clkinv_1 u_node_11 (.A(node_10), .Y(node_11));
  sky130_fd_sc_hd__a21oi_1 u_node_12 (.A1(c), .A2(node_6), .Y(node_12));
  sky130_fd_sc_hd__clkinv_1 u_node_13 (.A(node_12), .Y(node_13));
  sky130_fd_sc_hd__clkinv_1 u_node_14 (.A(d), .Y(node_14));
  sky130_fd_sc_hd__a21oi_1 u_node_15 (.A1(node_13), .A2(node_14), .Y(node_15));
  sky130_fd_sc_hd__clkinv_1 u_node_16 (.A(node_15), .Y(node_16));
endmodule
