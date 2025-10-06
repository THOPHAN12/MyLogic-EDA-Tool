"""
MyLogic Commands cho Logic Tổ hợp

Danh sách đầy đủ các lệnh MyLogic cho synthesis mạch logic tổ hợp.
Dựa trên tài liệu Yosys và synthesis flow.
"""

from typing import Dict, List, Optional


class MyLogicCommands:
    """MyLogic commands cho synthesis logic tổ hợp."""
    
    @staticmethod
    def get_synthesis_flow() -> List[str]:
        """Get complete Yosys synthesis flow for combinational logic."""
        return [
            "read_verilog <file>",     # Read Verilog files
            "hierarchy -check -top",  # Hierarchy processing
            "proc",                   # Process combinational logic
            "opt_expr",               # Expression optimization
            "opt_clean",              # Clean up
            "opt_muxtree",            # Multiplexer optimization
            "opt_reduce",             # Reduction optimization
            "memory",                 # Memory processing
            "opt",                    # General optimization
            "techmap",                # Technology mapping
            "abc",                    # ABC optimization
            "clean",                  # Final cleanup
            "stat",                   # Statistics
            "write_verilog <file>",   # Write Verilog output
            "write_json <file>",      # Write JSON output
            "write_blif <file>",       # Write BLIF output
        ]
    
    @staticmethod
    def get_optimization_commands() -> Dict[str, List[str]]:
        """Get optimization commands by category."""
        return {
            "Expression Optimization": [
                "opt_expr",           # Expression optimization
                "opt_expr_mux",       # Multiplexer expression optimization
                "opt_expr_clean",     # Clean expressions
            ],
            "Circuit Optimization": [
                "opt_clean",          # Clean up unused signals
                "opt_muxtree",        # Multiplexer tree optimization
                "opt_reduce",         # Reduction optimization
                "opt_merge",          # Merge optimization
                "opt_mem",            # Memory optimization
            ],
            "Technology Mapping": [
                "techmap",            # Technology mapping
                "techmap -map <lib>", # Map to specific library
                "abc",                # ABC optimization
                "abc -liberty <lib>", # ABC with liberty library
            ],
            "Analysis Commands": [
                "stat",               # Statistics
                "show",               # Show design
                "ls",                 # List modules
                "cd <module>",        # Change to module
            ],
            "Output Commands": [
                "write_verilog <file>", # Write Verilog
                "write_json <file>",    # Write JSON
                "write_blif <file>",    # Write BLIF
                "write_edif <file>",    # Write EDIF
                "write_spice <file>",   # Write SPICE
            ]
        }
    
    @staticmethod
    def get_combinational_specific_commands() -> List[str]:
        """Get commands specific to combinational logic."""
        return [
            "proc",                   # Process combinational logic
            "proc_clean",             # Clean processes
            "proc_rmdead",            # Remove dead processes
            "proc_init",              # Initialize processes
            "proc_arst",              # Async reset processes
            "proc_dlatch",            # D-latch processes
            "proc_dff",               # DFF processes
            "proc_mux",               # Multiplexer processes
            "proc_rom",               # ROM processes
        ]
    
    @staticmethod
    def get_abc_scripts() -> Dict[str, str]:
        """Get ABC optimization scripts."""
        return {
            "fast": "strash; ifraig; refactor; rewrite; balance;",
            "balanced": "strash; ifraig; refactor; rewrite; balance; map;",
            "thorough": "strash; ifraig; refactor; rewrite; balance; map;",
            "area": "strash; ifraig; refactor; rewrite; balance; map -a;",
            "delay": "strash; ifraig; refactor; rewrite; balance; map -d;",
            "mixed": "strash; ifraig; refactor; rewrite; balance; map -a -d;",
        }
    
    @staticmethod
    def get_liberty_mapping_commands() -> List[str]:
        """Get commands for liberty library mapping."""
        return [
            "read_liberty <lib>",      # Read liberty library
            "techmap -map <lib>",     # Map to library
            "abc -liberty <lib>",    # ABC with liberty
            "dfflibmap -liberty <lib>", # DFF library mapping
            "dfflibmap -liberty <lib> -dff", # DFF mapping
        ]
    
    @staticmethod
    def get_verification_commands() -> List[str]:
        """Get commands for design verification."""
        return [
            "equiv_opt",              # Equivalence optimization
            "equiv_make",             # Make equivalence
            "equiv_simple",           # Simple equivalence
            "equiv_status",           # Equivalence status
            "equiv_induct",           # Inductive equivalence
            "sat",                    # SAT solving
            "sat -verify",            # SAT verification
            "sat -prove",             # SAT proving
        ]
    
    @staticmethod
    def get_analysis_commands() -> List[str]:
        """Get commands for design analysis."""
        return [
            "stat",                   # Statistics
            "stat -top <module>",     # Top module statistics
            "stat -liberty <lib>",    # Liberty statistics
            "show",                   # Show design
            "show <module>",          # Show specific module
            "show -format dot",      # Show as DOT
            "show -format svg",       # Show as SVG
            "ls",                     # List modules
            "cd <module>",            # Change to module
            "pwd",                    # Print working directory
        ]


def demo_yosys_commands():
    """Demonstrate Yosys commands for combinational logic."""
    print("=" * 60)
    print("Yosys Commands for Combinational Logic")
    print("=" * 60)
    
    commands = YosysCombinationalCommands()
    
    print("\n1. Synthesis Flow:")
    for i, cmd in enumerate(commands.get_synthesis_flow(), 1):
        print(f"  {i:2d}. {cmd}")
    
    print("\n2. Optimization Commands:")
    opt_commands = commands.get_optimization_commands()
    for category, cmd_list in opt_commands.items():
        print(f"\n  {category}:")
        for cmd in cmd_list:
            print(f"    - {cmd}")
    
    print("\n3. Combinational-Specific Commands:")
    for cmd in commands.get_combinational_specific_commands():
        print(f"  - {cmd}")
    
    print("\n4. ABC Scripts:")
    abc_scripts = commands.get_abc_scripts()
    for name, script in abc_scripts.items():
        print(f"  {name}: {script}")
    
    print("\n5. Liberty Mapping Commands:")
    for cmd in commands.get_liberty_mapping_commands():
        print(f"  - {cmd}")
    
    print("\n6. Verification Commands:")
    for cmd in commands.get_verification_commands():
        print(f"  - {cmd}")
    
    print("\n7. Analysis Commands:")
    for cmd in commands.get_analysis_commands():
        print(f"  - {cmd}")


if __name__ == "__main__":
    demo_yosys_commands()
