// Intentional syntax error example for parser test
// This file aggregates multiple syntax errors to validate the parser:
// 1) Missing 'assign' keyword
// 2) Missing semicolon at end of statement
// 3) Missing semicolon even when 'assign' is present
// 4) Nonblocking assignment outside always (also missing semicolon)
module bad_syntax(input a, input b, output y);
    wire z;
    // Error 1: missing assign + missing semicolon
   assign y = a & b;

    // Error 2: has assign but missing semicolon
    assign z = a | b

    // Error 3: nonblocking assign outside procedural block, missing semicolon
    wire temp1;
    assign temp1 = a ^ b;

endmodule