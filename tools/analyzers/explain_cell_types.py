#!/usr/bin/env python3
"""
Giải thích các dạng cell trong MyLogic EDA Tool
"""

import json
import sys

def explain_cell_types():
    """Giải thích các dạng cell."""
    
    print("=== CELL TYPES IN MYLOGIC EDA TOOL ===")
    print()
    
    # Cell types từ MyLogic parser
    mylogic_cell_types = {
        "Logic Gates": {
            "AND": "Logic AND gate - output = A & B",
            "OR": "Logic OR gate - output = A | B", 
            "XOR": "Logic XOR gate - output = A ^ B",
            "NAND": "Logic NAND gate - output = !(A & B)",
            "NOR": "Logic NOR gate - output = !(A | B)",
            "NOT": "Logic NOT gate - output = !A",
            "BUF": "Buffer gate - output = A (signal amplification)"
        },
        "Arithmetic Operations": {
            "ADD": "Addition - output = A + B",
            "SUB": "Subtraction - output = A - B", 
            "MUL": "Multiplication - output = A * B",
            "DIV": "Division - output = A / B"
        },
        "Multiplexers": {
            "MUX": "Multiplexer - output = S ? A : B (S=select, A/B=inputs)"
        },
        "Module Instantiations": {
            "MODULE": "Module instantiation - calling another module"
        }
    }
    
    # Yosys cell types mapping
    yosys_mapping = {
        "AND": "$_AND_",
        "OR": "$_OR_", 
        "XOR": "$_XOR_",
        "NAND": "$_NAND_",
        "NOR": "$_NOR_",
        "NOT": "$_NOT_",
        "BUF": "$_BUF_",
        "ADD": "$_ADD_",
        "SUB": "$_SUB_",
        "MUL": "$_MUL_",
        "DIV": "$_DIV_",
        "MUX": "$_MUX_"
    }
    
    print("1. CELL TYPES FROM MYLOGIC PARSER:")
    print("=" * 50)
    
    for category, cells in mylogic_cell_types.items():
        print(f"\n{category}:")
        for cell_type, description in cells.items():
            print(f"  {cell_type:8} - {description}")
    
    print("\n2. YOSYS CELL TYPES MAPPING:")
    print("=" * 50)
    print("MyLogic Type  ->  Yosys Type")
    print("-" * 30)
    for mylogic_type, yosys_type in yosys_mapping.items():
        print(f"{mylogic_type:12} ->  {yosys_type}")
    
    print("\n3. CELL TYPES SOURCE:")
    print("=" * 50)
    print("• Logic Gates: From Verilog syntax (and, or, xor, nand, nor, not, buf)")
    print("• Arithmetic: From Verilog operators (+, -, *, /)")
    print("• Multiplexers: From ternary operator (? :) in Verilog")
    print("• Module Instantiations: From module calls in Verilog")
    
    print("\n4. HOW PARSER RECOGNIZES CELL TYPES:")
    print("=" * 50)
    print("• Verilog Operators -> Arithmetic cells (ADD, SUB, MUL, DIV)")
    print("• Verilog Gates -> Logic cells (AND, OR, XOR, NAND, NOR, NOT, BUF)")
    print("• Ternary Operator (? :) -> MUX cells")
    print("• Module Instantiations -> MODULE cells")
    
    print("\n5. EXAMPLE IN PRIORITY ENCODER:")
    print("=" * 50)
    
    # Load và phân tích priority encoder
    try:
        with open("examples/priority_encoder_netlist.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        netlist = data['netlist']
        nodes = netlist.get('nodes', [])
        
        print("Cell types found in priority_encoder.v:")
        cell_counts = {}
        for node in nodes:
            node_type = node.get('type', 'UNKNOWN')
            cell_counts[node_type] = cell_counts.get(node_type, 0) + 1
        
        for cell_type, count in cell_counts.items():
            description = mylogic_cell_types.get("Logic Gates", {}).get(cell_type, 
                       mylogic_cell_types.get("Multiplexers", {}).get(cell_type,
                       mylogic_cell_types.get("Arithmetic Operations", {}).get(cell_type, "Unknown")))
            print(f"  {cell_type}: {count} cells - {description}")
            
    except Exception as e:
        print(f"[ERROR] Cannot analyze priority encoder: {e}")

def analyze_specific_file(json_file):
    """Phân tích cell types trong file cụ thể."""
    
    print(f"\n=== PHÂN TÍCH CELL TYPES TRONG {json_file} ===")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'netlist' in data:
            netlist = data['netlist']
        else:
            netlist = data
        
        nodes = netlist.get('nodes', [])
        
        if not nodes:
            print("No nodes found in file")
            return
        
        print(f"Total nodes: {len(nodes)}")
        print()
        
        # Phân tích từng node
        for i, node in enumerate(nodes):
            node_id = node.get('id', f'node_{i}')
            node_type = node.get('type', 'UNKNOWN')
            fanins = node.get('fanins', [])
            
            print(f"Node {i+1}: {node_id}")
            print(f"  Type: {node_type}")
            print(f"  Fanins: {len(fanins)}")
            
            if fanins:
                for j, fanin in enumerate(fanins):
                    if isinstance(fanin, list) and len(fanin) >= 1:
                        fanin_signal = fanin[0]
                        fanin_inverted = fanin[1] if len(fanin) > 1 else False
                        print(f"    Fanin {j+1}: {fanin_signal} (inverted: {fanin_inverted})")
            
            print()
            
    except Exception as e:
        print(f"[ERROR] Cannot analyze file: {e}")

def main():
    explain_cell_types()
    
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        analyze_specific_file(json_file)

if __name__ == "__main__":
    main()
