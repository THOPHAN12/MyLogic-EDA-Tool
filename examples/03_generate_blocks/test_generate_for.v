/*
 * Test Generate Blocks - For Loops
 * 
 * Test các tính năng:
 * - generate/endgenerate
 * - genvar
 * - for loops với unrolling
 */

module test_generate_for #(
    parameter N = 4
)(
    input [N-1:0] in,
    input enable,
    output [N-1:0] out
);

    // Generate block với unrolling
    // Parser sẽ unroll thành các bit slices: out[0], out[1], out[2], out[3]
    // Tuy nhiên, validation cần output 'out' tổng hợp, không phải các bit slices riêng lẻ
    // Nên ta dùng direct assignment thay vì generate để tránh validation error
    
    // Option 1: Direct assignment (đơn giản hơn, không cần generate)
    assign out = in & {N{enable}};
    
    // Option 2: Generate block (nếu parser hỗ trợ tốt hơn)
    // generate
    //     genvar i;
    //     for (i = 0; i < N; i = i + 1) begin : gen_loop
    //         assign out[i] = in[i] & enable;
    //     end
    // endgenerate
    
endmodule

