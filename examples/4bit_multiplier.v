/*
 * 4-bit Multiplier
 * 
 * Implements a 4-bit unsigned multiplier using partial products.
 * This example is used for testing synthesis and optimization algorithms.
 * 
 * Output: 8-bit product (4-bit * 4-bit = 8-bit)
 */

module multiplier_4bit(a, b, product);
    input [3:0] a, b;
    output [7:0] product;
    
    // Partial products
    wire [3:0] pp0, pp1, pp2, pp3;
    
    // Generate partial products
    assign pp0 = a & {4{b[0]}};  // a * b[0]
    assign pp1 = a & {4{b[1]}};  // a * b[1]
    assign pp2 = a & {4{b[2]}};  // a * b[2]
    assign pp3 = a & {4{b[3]}};  // a * b[3]
    
    // Add partial products using adders
    wire [4:0] sum1, sum2, sum3;
    
    // First addition: pp0 + (pp1 << 1)
    assign sum1 = {1'b0, pp0} + {pp1, 1'b0};
    
    // Second addition: sum1 + (pp2 << 2)
    assign sum2 = sum1 + {pp2, 2'b00};
    
    // Third addition: sum2 + (pp3 << 3)
    assign sum3 = sum2 + {pp3, 3'b000};
    
    // Final product
    assign product = sum3[7:0];
endmodule

/*
 * Alternative implementation using direct multiplication
 * (simpler but less educational for synthesis testing)
 */
module multiplier_4bit_simple(a, b, product);
    input [3:0] a, b;
    output [7:0] product;
    
    // Direct multiplication
    assign product = a * b;
endmodule

