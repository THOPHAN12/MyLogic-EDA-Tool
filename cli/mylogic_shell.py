"""
MyLogic interactive shell – CLI chính cho công cụ tổng hợp luận lý.

Cung cấp: đọc Verilog, synthesis (Netlist → AIG), tối ưu (Strash, DCE, CSE, ConstProp, Balance),
technology mapping, complete flow, thống kê và xuất netlist.
"""

import os
import sys
import logging
from typing import Any, Dict, Optional, Union

# Thêm thư mục gốc project vào đường dẫn
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers import parse_verilog

class MyLogicShell:
    """Shell tương tác chính của MyLogic EDA Tool (tổng hợp luận lý, tối ưu, ánh xạ công nghệ)."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Khởi tạo shell với trạng thái trống và cấu hình tùy chọn."""
        self.netlist: Optional[Union[Dict[str, Any], Any]] = None
        self.current_netlist: Optional[Union[Dict[str, Any], Any]] = None
        self.current_aig = None  # AIG object sau synthesis
        self.filename: Optional[str] = None
        self.history: list = []
        self.config = config or {}
        
        # Áp dụng cấu hình
        self.prompt = self.config.get("shell", {}).get("prompt", "mylogic> ")
        self.history_size = self.config.get("shell", {}).get("history_size", 1000)
        self.auto_complete = self.config.get("shell", {}).get("auto_complete", True)
        self.color_output = self.config.get("shell", {}).get("color_output", True)
        self.auto_export_json = self.config.get("shell", {}).get("auto_export_json", True)  # Mặc định bật
        
        # Khởi tạo từ điển commands
        self.commands = {
            'read': self._read_file,
            'stats': self._show_stats,
            'vectors': self._show_vector_details,
            'nodes': self._show_node_details,
            'wires': self._show_wire_details,
            'modules': self._show_module_details,
            'export': self._export_json,
            'export_json': self._export_json,
            'history': self._show_history,
            'clear': self._clear_screen,
            'help': self._show_help,
            'exit': self._exit_shell,
            'dump': self._dump_ast,
            'dump_ast': self._dump_ast,
        # Logic Synthesis algorithms (phạm vi đề tài: Strash, DCE, CSE, ConstProp, Balance, Techmap)
        'strash': self._run_strash,
        'cse': self._run_cse,
        'constprop': self._run_constprop,
        'balance': self._run_balance,
        'synthesis': self._run_synthesis,
        'optimize': self._run_optimization,
        'dce': self._run_dce,
        'aig': self._run_aig,
        'techmap': self._run_technology_mapping,
        'complete_flow': self._run_complete_flow,
        'workflow': self._run_complete_flow  # Alias
        }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        
        # Yosys integration removed

    def run(self):
        """Chạy interactive shell."""
        print("Welcome to MyLogic Shell. Type 'help' for commands.")
        while True:
            try:
                cmd = input(self.prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting.")
                break
            except Exception as e:
                print(f"[ERROR] Input error: {e}")
                continue

            if not cmd:
                continue

            # Thêm vào history
            self.history.append(cmd)
            
            parts = cmd.split()
            op = parts[0]

            # Kiểm tra xem command có tồn tại trong từ điển commands không
            if op in self.commands:
                try:
                    self.commands[op](parts)
                except Exception as e:
                    print(f"[ERROR] Command error: {e}")
            else:
                print(f"[ERROR] Unknown command: {op}")
                print("Type 'help' for available commands.")

    def _read_file(self, parts):
        """Đọc file Verilog và tự động export JSON nếu được bật."""
        if len(parts) < 2:
            print("[ERROR] Usage: read <file>")
            return
        
        path = parts[1]
        try:
            if path.endswith(".v"):
                self.netlist = parse_verilog(path)
                self.current_netlist = self.netlist
                self.filename = path
                n_nodes = len(self.netlist.get('nodes', []))
                print(f"[OK] Loaded vector netlist with {n_nodes} nodes.")
            else:
                # Fallback cho các loại file khác
                self.netlist = parse_verilog(path)
                self.current_netlist = self.netlist
                self.filename = path
                n_nodes = len(self.netlist.get('nodes', []))
                print(f"[OK] Loaded netlist with {n_nodes} nodes.")
            
            # Tự động export JSON nếu được bật
            if self.auto_export_json and self.current_netlist:
                self._auto_export_json()
                
        except Exception as e:
            msg = str(e)
            if "Syntax error" in msg:
                print(f"ERROR SYNTAX: {msg}")
            else:
                print(f"[ERROR] Failed to read file: {msg}")

    def _show_stats(self, parts=None):
        """Enhanced circuit statistics with detailed analysis."""
        # Use current_netlist if available, otherwise use netlist
        netlist_to_show = self.current_netlist if self.current_netlist else self.netlist
        
        if not netlist_to_show:
            print("[WARNING] No netlist loaded.")
            return
        
        if isinstance(netlist_to_show, dict):
            # Vector netlist
            name = netlist_to_show.get('name', 'unknown')
            inputs = netlist_to_show.get('inputs', [])
            outputs = netlist_to_show.get('outputs', [])
            nodes = netlist_to_show.get('nodes', [])
            wires = netlist_to_show.get('wires', [])
            vector_widths = netlist_to_show.get('attrs', {}).get('vector_widths', {})
            
            print("=== ENHANCED CIRCUIT STATISTICS ===")
            print(f"  Name    : {name}")
            print(f"  Inputs  : {len(inputs)}")
            print(f"  Outputs : {len(outputs)}")
            print(f"  Wires   : {len(wires)}")
            print(f"  Nodes   : {len(nodes)}")
            
            # Enhanced vector widths analysis
            if vector_widths:
                print("\n  Vector Analysis:")
                # Group by width for better readability
                width_groups = {}
                for signal, width in vector_widths.items():
                    if width not in width_groups:
                        width_groups[width] = []
                    width_groups[width].append(signal)
                
                # Display grouped by width - show all signals with detailed info
                for width in sorted(width_groups.keys(), reverse=True):
                    signals = width_groups[width]
                    print(f"    {width}-bit ({len(signals)} signals): {', '.join(signals)}")
                
                # Enhanced summary
                total_signals = len(vector_widths)
                unique_widths = len(width_groups)
                print(f"  Summary: {total_signals} signals across {unique_widths} bit widths")
            
            # Enhanced node analysis
            if nodes:
                node_types = {}
                for node in nodes:
                    node_type = node.get('type', 'UNKNOWN')
                    node_types[node_type] = node_types.get(node_type, 0) + 1
                
                print("\n  Node Analysis:")
                for node_type, count in sorted(node_types.items()):
                    percentage = (count / len(nodes)) * 100
                    print(f"    {node_type}: {count} ({percentage:.1f}%)")
            
            # Wire analysis
            if wires:
                print(f"\n  Wire Analysis:")
                print(f"    Total wires: {len(wires)}")
                # Analyze wire types if available
                wire_types = {}
                for wire in wires:
                    if isinstance(wire, dict):
                        wire_type = wire.get('type', 'unknown')
                        wire_types[wire_type] = wire_types.get(wire_type, 0) + 1
                    else:
                        wire_types['simple'] = wire_types.get('simple', 0) + 1
                
                for wire_type, count in wire_types.items():
                    print(f"    {wire_type}: {count}")
            
            # Module instantiation analysis
            module_insts = netlist_to_show.get('attrs', {}).get('module_instantiations', {})
            if module_insts:
                print(f"\n  Module Instantiations:")
                print(f"    Total modules: {len(module_insts)}")
                for inst_name, inst_info in module_insts.items():
                    module_type = inst_info.get('module_type', 'unknown')
                    connections = inst_info.get('connections', [])
                    print(f"    {inst_name} ({module_type}): {len(connections)} connections")
            
            print(f"\n  Type    : Vector (n-bit)")
            print("  Use 'vectors' command for detailed view")
            print("  Use 'nodes' command for node details")
            print("  Use 'wires' command for wire analysis")
        else:
            # Scalar netlist object
            print("Circuit statistics:")
            print(f"  Name    : {getattr(self.netlist, 'name', 'unknown')}")
            print(f"  Inputs  : {len(getattr(self.netlist, 'inputs', []))}")
            print(f"  Outputs : {len(getattr(self.netlist, 'outputs', []))}")
            print(f"  Wires   : {len(getattr(self.netlist, 'wires', []))}")
            print(f"  Nodes   : {len(getattr(self.netlist, 'nodes', []))}")
            print(f"  Type    : Scalar (1-bit)")

    def _show_vector_details(self, parts=None):
        """Hiển thị chi tiết vector widths."""
        if not self.netlist:
            print("[WARNING] No netlist loaded.")
            return
        
        if isinstance(self.netlist, dict):
            vector_widths = self.netlist.get('attrs', {}).get('vector_widths', {})
            if not vector_widths:
                print("No vector information available.")
                return
            
            print("Detailed Vector Widths:")
            # Group by width
            width_groups = {}
            for signal, width in vector_widths.items():
                if width not in width_groups:
                    width_groups[width] = []
                width_groups[width].append(signal)
            
            # Display all signals grouped by width
            for width in sorted(width_groups.keys(), reverse=True):
                signals = width_groups[width]
                print(f"\n{width}-bit signals ({len(signals)} total):")
                for i, signal in enumerate(signals, 1):
                    print(f"  {i:2d}. {signal}")
        else:
            print("Vector details only available for vector netlists.")

    def _show_history(self, parts=None):
        """Hiển thị lịch sử commands."""
        if not self.history:
            print("No commands in history.")
            return
        
        print("Command history:")
        for i, cmd in enumerate(self.history[-10:], 1):
            print(f"  {i:2d}. {cmd}")

    def _clear_screen(self, parts=None):
        """Xóa màn hình."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _show_help(self, parts=None):
        """Enhanced help with all available commands."""
        print("=== ENHANCED MYLOGIC EDA TOOL COMMANDS ===")
        print()
        print("File Operations:")
        print("  read <file>           - Load a .logic or .v file (auto-exports JSON to outputs/)")
        print("  stats                 - Enhanced circuit statistics")
        print("  vectors               - Detailed vector width analysis")
        print("  nodes                 - Detailed node information")
        print("  wires                 - Detailed wire analysis")
        print("  modules               - Module instantiation details")
        print("  export [file]         - Export netlist to JSON file (manual export)")
        print("  dump / dump_ast       - Dump netlist structure as AST tree (like Yosys)")
        print()
        print("Logic Synthesis:")
        print("  synthesis             - Netlist -> AIG")
        print("  strash                - Structural hashing")
        print("  dce [level]          - Dead code elimination")
        print("  cse                  - Common subexpression elimination")
        print("  constprop            - Constant propagation")
        print("  balance              - Logic balancing")
        print("  optimize             - AIG optimization (Strash, DCE, CSE, ConstProp, Balance)")
        print("  techmap [strategy]   - Technology mapping (area/delay/balanced)")
        print("  complete_flow [strategy] [library] - Full flow")
        print("  aig <op>              - AIG (create/strash/convert/stats)")
        print()
        print("Utility: stats, vectors, nodes, wires, modules, export, history, clear, help, exit")

    def _exit_shell(self, parts=None):
        """Thoát khỏi shell."""
        print("Goodbye.")
        sys.exit(0)
    
    def _run_strash(self, parts=None):
        """Chạy Structural Hashing optimization."""
        if not self.current_netlist:
            print("[ERROR] No netlist loaded. Use 'read <file>' first.")
            return
        
        try:
            from core.synthesis.strash import StrashOptimizer
            
            print("[INFO] Running Structural Hashing optimization...")
            original_nodes = len(self.current_netlist.get('nodes', {}))
            
            optimizer = StrashOptimizer()
            optimized_netlist = optimizer.optimize(self.current_netlist)
            self.current_netlist = optimized_netlist
            
            optimized_nodes = len(optimized_netlist.get('nodes', {}))
            
            print(f"[OK] Structural Hashing completed!")
            print(f"  Original: {original_nodes} nodes")
            print(f"  Optimized: {optimized_nodes} nodes")
            print(f"  Removed: {original_nodes - optimized_nodes} nodes")
            
        except ImportError:
            print("[ERROR] Strash module not available")
        except Exception as e:
            print(f"[ERROR] Structural Hashing failed: {e}")
    
    def _run_cse(self, parts=None):
        """Chạy Common Subexpression Elimination."""
        if not self.current_netlist:
            print("[ERROR] No netlist loaded. Use 'read <file>' first.")
            return
        
        try:
            from core.optimization.cse import CSEOptimizer
            
            # Suppress verbose logging and Unicode issues for CSE module
            cse_logger = logging.getLogger('core.optimization.cse')
            cse_logger.setLevel(logging.ERROR)
            cse_logger.propagate = False

            print("[INFO] Running Common Subexpression Elimination...")
            original_nodes = len(self.current_netlist.get('nodes', {}))
            
            optimizer = CSEOptimizer()
            optimized_netlist = optimizer.optimize(self.current_netlist)
            self.current_netlist = optimized_netlist
            
            optimized_nodes = len(optimized_netlist.get('nodes', {}))
            
            print(f"[OK] CSE optimization completed!")
            print(f"  Original: {original_nodes} nodes")
            print(f"  Optimized: {optimized_nodes} nodes")
            print(f"  Removed: {original_nodes - optimized_nodes} nodes")
            
        except ImportError:
            print("[ERROR] CSE module not available")
        except Exception as e:
            print(f"[ERROR] CSE optimization failed: {e}")
    
    def _run_constprop(self, parts=None):
        """Chạy Constant Propagation."""
        if not self.current_netlist:
            print("[ERROR] No netlist loaded. Use 'read <file>' first.")
            return
        
        try:
            from core.optimization.constprop import ConstPropOptimizer
            
            # Suppress verbose logging and Unicode issues for ConstProp module
            cp_logger = logging.getLogger('core.optimization.constprop')
            cp_logger.setLevel(logging.ERROR)
            cp_logger.propagate = False

            print("[INFO] Running Constant Propagation...")
            original_nodes = len(self.current_netlist.get('nodes', {}))
            
            optimizer = ConstPropOptimizer()
            optimized_netlist = optimizer.optimize(self.current_netlist)
            self.current_netlist = optimized_netlist
            
            optimized_nodes = len(optimized_netlist.get('nodes', {}))
            
            print(f"[OK] Constant Propagation completed!")
            print(f"  Original: {original_nodes} nodes")
            print(f"  Optimized: {optimized_nodes} nodes")
            print(f"  Simplified: {original_nodes - optimized_nodes} nodes")
            
        except ImportError:
            print("[ERROR] ConstProp module not available")
        except Exception as e:
            print(f"[ERROR] Constant Propagation failed: {e}")
    
    def _run_balance(self, parts=None):
        """Chạy Logic Balancing."""
        if not self.current_netlist:
            print("[ERROR] No netlist loaded. Use 'read <file>' first.")
            return
        
        try:
            from core.optimization.balance import BalanceOptimizer
            
            # Suppress verbose logging and Unicode issues for Balance module
            bal_logger = logging.getLogger('core.optimization.balance')
            bal_logger.setLevel(logging.ERROR)
            bal_logger.propagate = False

            print("[INFO] Running Logic Balancing...")
            original_nodes = len(self.current_netlist.get('nodes', {}))
            
            optimizer = BalanceOptimizer()
            optimized_netlist = optimizer.optimize(self.current_netlist)
            self.current_netlist = optimized_netlist
            
            optimized_nodes = len(optimized_netlist.get('nodes', {}))
            
            print(f"[OK] Logic Balancing completed!")
            print(f"  Original: {original_nodes} nodes")
            print(f"  Balanced: {optimized_nodes} nodes")
            print(f"  Added: {optimized_nodes - original_nodes} nodes")
            
        except ImportError:
            print("[ERROR] Balance module not available")
        except Exception as e:
            print(f"[ERROR] Logic Balancing failed: {e}")
    
    def _run_synthesis(self, parts):
        """Chạy Synthesis: Netlist -> AIG conversion."""
        if not self.current_netlist:
            print("[ERROR] No netlist loaded. Use 'read <file>' first.")
            return
        
        try:
            from core.synthesis.synthesis_flow import synthesize
            
            print("[INFO] Running Synthesis: Netlist -> AIG conversion...")
            
            # Count original nodes
            nodes_data = self.current_netlist.get('nodes', {})
            if isinstance(nodes_data, dict):
                original_nodes = len(nodes_data)
            elif isinstance(nodes_data, list):
                original_nodes = len(nodes_data)
            else:
                original_nodes = 0
            
            # Convert Netlist -> AIG
            self.current_aig = synthesize(self.current_netlist)
            
            # Print results
            print(f"[OK] Synthesis completed!")
            print(f"  Netlist nodes: {original_nodes}")
            print(f"  AIG nodes: {self.current_aig.count_nodes()}")
            print(f"  AIG AND nodes: {self.current_aig.count_and_nodes()}")
            print(f"  Primary inputs: {len(self.current_aig.pis)}")
            print(f"  Primary outputs: {len(self.current_aig.pos)}")
            print(f"[INFO] Next step: Run 'optimize <level>' to optimize AIG")
            
        except ImportError:
            print("[ERROR] Synthesis module not available")
        except Exception as e:
            print(f"[ERROR] Synthesis failed: {e}")
            import traceback
            traceback.print_exc()
    
    def _run_optimization(self, parts):
        """Chạy Optimization: AIG optimization (một chuẩn duy nhất)."""
        if not self.current_aig:
            print("[ERROR] No AIG available. Run 'synthesis' first to convert Netlist -> AIG.")
            return
        
        try:
            from core.optimization.optimization_flow import optimize
            
            print("[INFO] Running AIG Optimization...")
            original_nodes = self.current_aig.count_nodes()
            
            self.current_aig = optimize(self.current_aig)
            
            final_nodes = self.current_aig.count_nodes()
            reduction = original_nodes - final_nodes
            
            print(f"[OK] AIG Optimization completed!")
            print(f"  Original AIG nodes: {original_nodes}")
            print(f"  Optimized AIG nodes: {final_nodes}")
            if original_nodes > 0:
                print(f"  Total reduction: {reduction} nodes ({(reduction/original_nodes)*100:.1f}%)")
            
        except ImportError:
            print("[ERROR] Optimization module not available")
        except Exception as e:
            print(f"[ERROR] Optimization failed: {e}")
            import traceback
            traceback.print_exc()
    
    def _run_dce(self, parts):
        """Chạy Dead Code Elimination optimization."""
        if not parts or len(parts) < 2:
            print("Usage: dce <level>")
            print("Levels: basic, advanced, aggressive")
            return
        
        level = parts[1].lower()
        if level not in ["basic", "advanced", "aggressive"]:
            print("Invalid DCE level. Use: basic, advanced, or aggressive")
            return
        
        if not self.current_netlist:
            print("[ERROR] No netlist loaded. Use 'read <file>' first.")
            return
        
        try:
            from core.optimization.dce import DCEOptimizer
            
            print(f"[INFO] Running DCE optimization (level: {level})...")
            original_nodes = len(self.current_netlist.get('nodes', {}))
            original_wires = len(self.current_netlist.get('wires', []))
            
            optimizer = DCEOptimizer()
            optimized_netlist = optimizer.optimize(self.current_netlist, level)
            self.current_netlist = optimized_netlist
            
            optimized_nodes = len(optimized_netlist.get('nodes', {}))
            optimized_wires = len(optimized_netlist.get('wires', []))
            
            print(f"[OK] DCE optimization completed!")
            print(f"  Original: {original_nodes} nodes, {original_wires} wires")
            print(f"  Optimized: {optimized_nodes} nodes, {optimized_wires} wires")
            print(f"  Removed: {original_nodes - optimized_nodes} nodes, {original_wires - optimized_wires} wires")
            
        except ImportError:
            print("[ERROR] DCE module not available")
        except Exception as e:
            print(f"[ERROR] DCE optimization failed: {e}")
    
    def _run_technology_mapping(self, parts):
        """Chạy technology mapping."""
        if not parts or len(parts) < 2:
            print("Usage: techmap <strategy> [library_file|library_type]")
            print("Strategies: area, delay, balanced")
            print("Library options:")
            print("  - Path to .lib, .json, or .v file")
            print("  - Library type (auto-detect from techlibs/):")
            print("    * asic          - ASIC standard cells")
            print("    * sky130       - SKY130 PDK (High Density)")
            print("    * fpga          - Auto-scan all FPGA libraries")
            print("    * fpga_common   - FPGA common cells")
            print("    * anlogic       - Anlogic FPGA")
            print("    * gowin         - Gowin FPGA")
            print("    * ice40         - Lattice iCE40")
            print("    * intel         - Intel/Altera FPGA")
            print("    * lattice       - Lattice FPGA")
            print("    * xilinx        - Xilinx FPGA")
            print("  Examples:")
            print("    techmap area                    # Auto-detect (ASIC first)")
            print("    techmap area asic               # Use techlibs/asic/")
            print("    techmap area fpga               # Auto-scan all FPGA")
            print("    techmap area fpga_common        # Use techlibs/fpga/common/")
            print("    techmap area ice40              # Use techlibs/fpga/ice40/")
            print("    techmap area xilinx             # Use techlibs/fpga/xilinx/")
            print("    techmap balanced techlibs/asic/standard_cells.lib")
            print("")
            print("Note: Techmap requires AIG from synthesis or optimization.")
            print("      Run 'synthesis' or 'optimize <level>' first.")
            return
        
        if not self.current_aig:
            print("[ERROR] No AIG available. Run 'synthesis' first to convert Netlist -> AIG.")
            print("        Or run 'optimize <level>' if you have an AIG.")
            return
        
        strategy = parts[1].lower()
        library_path = parts[2] if len(parts) > 2 else None
        
        # Normalize strategy name
        strategy_map = {
            "area": "area_optimal",
            "delay": "delay_optimal",
            "balanced": "balanced"
        }
        strategy = strategy_map.get(strategy, strategy)
        
        try:
            from core.technology_mapping.technology_mapping import (
                techmap, create_standard_library, load_library_from_file
            )
            import os
            
            print(f"[INFO] Running technology mapping with {strategy} strategy...")
            print(f"[INFO] Input AIG: {self.current_aig.count_nodes()} nodes, {self.current_aig.count_and_nodes()} AND nodes")
            
            # Load library từ file hoặc tự động tìm trong techlibs/
            library = None  # Initialize library variable
            library_type = None
            if library_path:
                # Kiểm tra xem có phải là library type không
                valid_types = ["asic", "fpga", "fpga_common", "anlogic", "gowin", 
                              "ice40", "intel", "lattice", "xilinx"]
                if library_path.lower() in valid_types:
                    library_type = library_path.lower()
                    library = self._try_load_default_library(library_type)
                elif os.path.exists(library_path):
                    # Đường dẫn file hợp lệ
                    print(f"[INFO] Loading library from: {library_path}")
                    try:
                        library = load_library_from_file(library_path)
                        print(f"[OK] Loaded library '{library.name}' with {len(library.cells)} cells")
                    except Exception as e:
                        print(f"[WARNING] Failed to load library from file: {e}")
                        print("[INFO] Trying to find library in techlibs/...")
                        library = self._try_load_default_library(library_type or "auto")
                else:
                    # File không tồn tại
                    print(f"[WARNING] Library file not found: {library_path}")
                    print("[INFO] Trying to find library in techlibs/...")
                    library = self._try_load_default_library("auto")
            else:
                # Không có library_path, tự động tìm
                print("[INFO] No library specified, trying to find library in techlibs/...")
                library = self._try_load_default_library("auto")
            
            # Ensure library is not None before using
            if library is None:
                print("[WARNING] No library loaded, using standard library")
                library = create_standard_library()
            
            # Use new techmap() function that takes AIG as input
            results = techmap(self.current_aig, library, strategy)
            
            # Print mapping report
            print("\n" + "="*60)
            print("TECHNOLOGY MAPPING REPORT")
            print("="*60)
            print(f"Mapping Strategy: {results['strategy']}")
            print(f"Input AIG nodes: {results.get('input_aig_nodes', 'N/A')}")
            print(f"Input AIG AND nodes: {results.get('input_aig_and_nodes', 'N/A')}")
            print(f"Converted LogicNodes: {results.get('converted_logic_nodes', 'N/A')}")
            print(f"Total Nodes: {results['total_nodes']}")
            print(f"Mapped Nodes: {results['mapped_nodes']}")
            print(f"Mapping Success Rate: {results['mapping_success_rate']*100:.1f}%")
            if 'total_area' in results:
                print(f"Total Area: {results['total_area']:.2f}")
            if 'total_delay' in results:
                print(f"Total Delay: {results['total_delay']:.2f}")
            print(f"Library: {results.get('library_name', 'N/A')}")
            print("="*60)
            
            print("[OK] Technology mapping completed")
            print("[INFO] Techmap is now independent: AIG -> Technology-mapped netlist")
            
        except ImportError:
            print("[ERROR] Technology mapping module not available")
        except Exception as e:
            print(f"[ERROR] Technology mapping failed: {e}")
    
    def _run_complete_flow(self, parts):
        """Chạy complete flow: Synthesis -> Optimization -> Technology Mapping (một chuẩn duy nhất)."""
        if not parts:
            print("Usage: complete_flow [techmap_strategy] [techmap_library]")
            print("  techmap_strategy: area, delay, balanced (default: area)")
            print("  techmap_library: library path or type (optional, default: auto)")
            print("")
            print("Examples:")
            print("  complete_flow                    # area techmap, auto library")
            print("  complete_flow delay               # delay-optimal techmap")
            print("  complete_flow area asic           # area techmap, ASIC library")
            print("  complete_flow balanced sky130    # balanced techmap, SKY130 library")
            return
        
        if not self.current_netlist:
            print("[ERROR] No netlist loaded. Use 'read <file>' first.")
            return
        
        # Parse arguments - separate flags from positional args
        positional_args = [p for p in parts[1:] if not p.startswith('--') and not p.startswith('-')]
        # flags kept for backward compatibility; no simulation/verification flags supported
        flags = [p for p in parts[1:] if p.startswith('--') or p.startswith('-')]
        
        techmap_strategy = positional_args[0].lower() if len(positional_args) > 0 else "area"
        techmap_strategy_map = {
            "area": "area_optimal",
            "delay": "delay_optimal",
            "balanced": "balanced"
        }
        techmap_strategy = techmap_strategy_map.get(techmap_strategy, techmap_strategy)
        
        techmap_library_path = positional_args[1] if len(positional_args) > 1 else None
        
        try:
            from core.complete_flow import run_complete_flow
            from core.technology_mapping.technology_mapping import (
                load_library_from_file, create_standard_library
            )
            import os
            
            print("=" * 70)
            print("COMPLETE FLOW: Synthesis -> Optimization -> Technology Mapping")
            print("=" * 70)
            print(f"Techmap strategy: {techmap_strategy}")
            print("")
            
            # Load library if specified
            library = None
            if techmap_library_path:
                valid_types = ["asic", "sky130", "fpga", "fpga_common", "anlogic", "gowin", 
                              "ice40", "intel", "lattice", "xilinx"]
                if techmap_library_path.lower() in valid_types:
                    # Library type
                    library = self._try_load_default_library(techmap_library_path.lower())
                elif os.path.exists(techmap_library_path):
                    # Library file path
                    library = load_library_from_file(techmap_library_path)
                else:
                    print(f"[WARNING] Library path not found: {techmap_library_path}")
                    print("[INFO] Will use auto-detected library")
            
            # Run complete flow (một chuẩn duy nhất)
            results = run_complete_flow(
                self.current_netlist,
                techmap_strategy=techmap_strategy,
                techmap_library=library,
                enable_optimization=True,
                enable_techmap=True,
            )
                
            # Update current AIG to the final AIG (from optimization or synthesis)
            if results['optimization'].get('enabled') and results['optimization'].get('aig'):
                self.current_aig = results['optimization']['aig']
            elif results['synthesis'].get('aig'):
                self.current_aig = results['synthesis']['aig']
            
            # Print summary
            print("\n" + "=" * 70)
            print("COMPLETE FLOW RESULTS SUMMARY")
            print("=" * 70)
            
            # Synthesis results
            synth_stats = results['synthesis']['stats']
            print(f"\n[1] Synthesis:")
            print(f"    Netlist nodes: {synth_stats['netlist_nodes']}")
            print(f"    AIG nodes: {synth_stats['aig_nodes']}")
            print(f"    AIG AND nodes: {synth_stats['aig_and_nodes']}")
            
            # Optimization results
            if results['optimization'].get('enabled') and results['optimization'].get('stats'):
                opt_stats = results['optimization']['stats']
                print(f"\n[2] Optimization:")
                print(f"    Before: {opt_stats['nodes_before']} nodes")
                print(f"    After: {opt_stats['nodes_after']} nodes")
                print(f"    Reduction: {opt_stats['reduction']} nodes ({opt_stats['reduction_percent']:.1f}%)")
            else:
                print(f"\n[2] Optimization: SKIPPED")
            
            # Techmap results
            if results['techmap'].get('enabled') and results['techmap'].get('results'):
                tm_results = results['techmap']['results']
                print(f"\n[3] Technology Mapping:")
                print(f"    Mapped: {tm_results['mapped_nodes']}/{tm_results['total_nodes']} nodes")
                print(f"    Success rate: {tm_results['mapping_success_rate']*100:.1f}%")
                if 'total_area' in tm_results:
                    print(f"    Total area: {tm_results['total_area']:.2f}")
                if 'total_delay' in tm_results:
                    print(f"    Total delay: {tm_results['total_delay']:.2f}")
            else:
                print(f"\n[3] Technology Mapping: SKIPPED")
            
            print("=" * 70)
            print("[OK] Complete flow finished successfully!")
            print("=" * 70)
            
        except ImportError as e:
            print(f"[ERROR] Complete flow module not available: {e}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"[ERROR] Complete flow failed: {e}")
            import traceback
            traceback.print_exc()
    
    def _try_load_default_library(self, library_type: str = "auto"):
        """
        Tự động tìm và load library từ techlibs/ nếu có.
        Fallback về standard library nếu không tìm thấy.
        
        Args:
            library_type: "auto", "asic", "sky130", "fpga", "fpga_common", "anlogic", 
                         "gowin", "ice40", "intel", "lattice", "xilinx"
        """
        from core.technology_mapping.technology_mapping import (
            create_standard_library, load_library_from_file
        )
        import os
        from pathlib import Path
        
        # Tìm project root (thư mục chứa mylogic.py hoặc cli/)
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent  # Từ cli/ lên Mylogic/
        
        # Định nghĩa các đường dẫn library theo loại
        library_paths = {
            "asic": [
                project_root / "techlibs" / "asic" / "standard_cells.json",
                project_root / "techlibs" / "asic" / "standard_cells.lib",
            ],
            "sky130": [
                project_root / "techlibs" / "asic" / "sky130" / "sky130_fd_sc_hd.json",  # JSON format (preferred)
                project_root / "techlibs" / "asic" / "sky130" / "sky130_fd_sc_hd.lib",   # Liberty format (fallback)
            ],
            "fpga_common": [
                project_root / "techlibs" / "fpga" / "common" / "cells.lib",
                project_root / "techlibs" / "fpga" / "common" / "cells.json",
            ],
            "anlogic": [
                project_root / "techlibs" / "fpga" / "anlogic" / "cells.lib",
                project_root / "techlibs" / "fpga" / "anlogic" / "cells.json",
            ],
            "gowin": [
                project_root / "techlibs" / "fpga" / "gowin" / "cells.lib",
                project_root / "techlibs" / "fpga" / "gowin" / "cells.json",
            ],
            "ice40": [
                project_root / "techlibs" / "fpga" / "ice40" / "cells.lib",
                project_root / "techlibs" / "fpga" / "ice40" / "cells.json",
            ],
            "intel": [
                project_root / "techlibs" / "fpga" / "intel" / "cells.lib",
                project_root / "techlibs" / "fpga" / "intel" / "cells.json",
                project_root / "techlibs" / "fpga" / "intel" / "common" / "cells.lib",
            ],
            "lattice": [
                project_root / "techlibs" / "fpga" / "lattice" / "cells.lib",
                project_root / "techlibs" / "fpga" / "lattice" / "cells.json",
            ],
            "xilinx": [
                project_root / "techlibs" / "fpga" / "xilinx" / "cells.lib",
                project_root / "techlibs" / "fpga" / "xilinx" / "cells.json",
            ],
        }
        
        # Xác định các đường dẫn cần thử
        default_paths = []
        
        if library_type == "auto" or library_type is None:
            # Tự động thử tất cả các đường dẫn (ưu tiên ASIC/SKY130 trước, sau đó là FPGA)
            default_paths = library_paths["asic"].copy()
            default_paths.extend(library_paths.get("sky130", []))
            # Thêm tất cả các FPGA libraries
            for fpga_type in ["fpga_common", "anlogic", "gowin", "ice40", "intel", "lattice", "xilinx"]:
                default_paths.extend(library_paths.get(fpga_type, []))
        elif library_type == "fpga":
            # Tự động scan tất cả các thư mục FPGA
            for fpga_type in ["fpga_common", "anlogic", "gowin", "ice40", "intel", "lattice", "xilinx"]:
                default_paths.extend(library_paths.get(fpga_type, []))
        elif library_type in library_paths:
            default_paths = library_paths[library_type]
        else:
            # Fallback về auto
            default_paths = library_paths["asic"].copy()
            for fpga_type in ["fpga_common", "anlogic", "gowin", "ice40", "intel", "lattice", "xilinx"]:
                default_paths.extend(library_paths.get(fpga_type, []))
        
        # Thử load từ các đường dẫn
        for lib_path in default_paths:
            if lib_path.exists():
                try:
                    print(f"[INFO] Found library in techlibs/: {lib_path}")
                    library = load_library_from_file(str(lib_path))
                    print(f"[OK] Loaded library '{library.name}' with {len(library.cells)} cells")
                    return library
                except Exception as e:
                    print(f"[WARNING] Failed to load {lib_path}: {e}")
                    continue
        
        # Nếu không tìm thấy trong techlibs/, dùng standard library
        print("[INFO] No library found in techlibs/, using standard library")
        return create_standard_library()
    
    def _show_node_details(self, parts=None):
        """Show detailed node information."""
        if not self.current_netlist:
            print("No netlist loaded. Use 'read <file>' first.")
            return
        
        netlist_to_show = self.current_netlist if self.current_netlist else self.netlist
        nodes = netlist_to_show.get('nodes', [])
        
        if not nodes:
            print("No nodes available.")
            return
        
        print("Detailed Node Information:")
        print("=" * 50)
        
        for i, node in enumerate(nodes):
            node_id = node.get('id', f'node_{i}')
            node_type = node.get('type', 'UNKNOWN')
            fanins = node.get('fanins', [])
            fanin_str = ', '.join([f'{f[0]}' for f in fanins]) if fanins else 'none'
            
            print(f"\n{i+1:2d}. {node_id} ({node_type})")
            print(f"     Inputs: [{fanin_str}]")
            
            # Show additional node attributes
            if 'module_type' in node:
                print(f"     Module: {node['module_type']}")
            if 'connections' in node:
                print(f"     Connections: {len(node['connections'])}")
        
        print(f"\nTotal: {len(nodes)} nodes")
    
    def _show_wire_details(self, parts=None):
        """Show detailed wire information."""
        if not self.current_netlist:
            print("No netlist loaded. Use 'read <file>' first.")
            return
        
        netlist_to_show = self.current_netlist if self.current_netlist else self.netlist
        wires = netlist_to_show.get('wires', [])
        
        if not wires:
            print("No wires available.")
            return
        
        print("Detailed Wire Information:")
        print("=" * 50)
        
        for i, wire in enumerate(wires):
            if isinstance(wire, dict):
                wire_id = wire.get('id', f'wire_{i}')
                wire_type = wire.get('type', 'unknown')
                source = wire.get('source', 'unknown')
                destination = wire.get('destination', 'unknown')
                
                print(f"\n{i+1:2d}. {wire_id} ({wire_type})")
                print(f"     Source: {source}")
                print(f"     Destination: {destination}")
            else:
                print(f"\n{i+1:2d}. {wire}")
        
        print(f"\nTotal: {len(wires)} wires")
    
    def _show_module_details(self, parts=None):
        """Show detailed module instantiation information."""
        if not self.current_netlist:
            print("No netlist loaded. Use 'read <file>' first.")
            return
        
        netlist_to_show = self.current_netlist if self.current_netlist else self.netlist
        module_insts = netlist_to_show.get('attrs', {}).get('module_instantiations', {})
        
        if not module_insts:
            print("No module instantiations available.")
            return
        
        print("Detailed Module Instantiation Information:")
        print("=" * 50)
        
        for i, (inst_name, inst_info) in enumerate(module_insts.items(), 1):
            module_type = inst_info.get('module_type', 'unknown')
            connections = inst_info.get('connections', [])
            
            print(f"\n{i:2d}. {inst_name} ({module_type})")
            print(f"     Connections: {len(connections)}")
            for j, conn in enumerate(connections):
                print(f"       {j+1}. {conn}")
        
        print(f"\nTotal: {len(module_insts)} module instantiations")
    
    def _dump_ast(self, parts=None):
        """
        Dump netlist structure dạng AST tree (tương tự Yosys -dump_ast).
        
        Prints netlist structure in tree format:
        - Module declaration
        - Ports (inputs/outputs)
        - Assignments với expression tree structure
        """
        if not self.current_netlist:
            netlist_to_show = self.netlist
            if not netlist_to_show:
                print("[ERROR] No netlist loaded. Use 'read <file>' first.")
                return
        else:
            netlist_to_show = self.current_netlist
        
        # Get netlist data
        if isinstance(netlist_to_show, dict):
            module_name = netlist_to_show.get('name', 'unknown')
            inputs = netlist_to_show.get('inputs', [])
            outputs = netlist_to_show.get('outputs', [])
            nodes = netlist_to_show.get('nodes', [])
            output_mapping = netlist_to_show.get('attrs', {}).get('output_mapping', {})
        else:
            print("[ERROR] Invalid netlist format.")
            return
        
        # Convert nodes to list if dict
        if isinstance(nodes, dict):
            nodes = list(nodes.values())
        
        print("Dumping Netlist AST Structure:")
        print("=" * 70)
        print(f"\nNETLIST_MODULE <{module_name}>")
        
        # Print ports
        for inp in inputs:
            print(f"  NETLIST_WIRE <{inp}> input port")
        
        for out in outputs:
            print(f"  NETLIST_WIRE <{out}> output port")
        
        # Build mappings:
        # 1. signal_to_node: output signal name -> node
        # 2. node_by_id: node_id -> node
        # 3. node_outputs: node_id -> output signal name
        signal_to_node = {}
        node_by_id = {}
        node_outputs = {}
        all_signals = set(inputs)  # Include inputs as valid signals
        
        for node in nodes:
            node_id = node.get('id', '')
            output = node.get('output', '')
            node_by_id[node_id] = node
            if output:
                signal_to_node[output] = node
                node_outputs[node_id] = output
                all_signals.add(output)
        
        # Build output assignments tree
        for output_name in outputs:
            print(f"\n  NETLIST_ASSIGN <{output_name}>")
            
            # Find node that drives this output
            node_id = output_mapping.get(output_name, '')
            node = None
            
            if node_id and node_id in node_by_id:
                node = node_by_id[node_id]
            elif output_name in signal_to_node:
                node = signal_to_node[output_name]
            else:
                # Try to find node by matching output name with node output
                for n in nodes:
                    if n.get('output') == output_name:
                        node = n
                        break
            
            if node:
                self._print_expression_tree(
                    node, nodes, signal_to_node, node_by_id, node_outputs,
                    all_signals, indent="    "
                )
            else:
                print(f"    NETLIST_IDENTIFIER <{output_name}>")
        
        print("\n--- END OF AST DUMP ---")
    
    def _print_expression_tree(self, node, all_nodes, signal_to_node, 
                               node_by_id, node_outputs, all_signals, indent=""):
        """
        Print expression tree cho một node (recursive).
        
        Args:
            node: Node dictionary
            all_nodes: List of all nodes
            signal_to_node: Dict mapping output signal names to nodes
            node_by_id: Dict mapping node_id to node
            node_outputs: Dict mapping node_id to output signal name
            all_signals: Set of all valid signal names (inputs + node outputs)
            indent: Current indentation string
        """
        node_type = node.get('type', 'UNKNOWN')
        node_id = node.get('id', '')
        output = node.get('output', '')
        
        # Get inputs
        inputs = node.get('inputs', [])
        fanins = node.get('fanins', [])
        
        # Determine input signals
        input_signals = []
        if fanins:
            for fanin in fanins:
                if isinstance(fanin, (list, tuple)) and len(fanin) > 0:
                    input_signals.append(str(fanin[0]))
                else:
                    input_signals.append(str(fanin))
        elif inputs:
            input_signals = [str(inp) for inp in inputs]
        
        # Map node type to AST-like format
        ast_type_map = {
            'AND': 'NETLIST_BIT_AND',
            'OR': 'NETLIST_BIT_OR',
            'XOR': 'NETLIST_BIT_XOR',
            'NAND': 'NETLIST_BIT_NAND',
            'NOR': 'NETLIST_BIT_NOR',
            'XNOR': 'NETLIST_BIT_XNOR',
            'NOT': 'NETLIST_BIT_NOT',
            'BUF': 'NETLIST_BUF',
            'ADD': 'NETLIST_ADD',
            'SUB': 'NETLIST_SUB',
            'MUL': 'NETLIST_MUL',
            'DIV': 'NETLIST_DIV',
            'EQ': 'NETLIST_EQ',
            'MUX': 'NETLIST_MUX',
        }
        
        ast_type = ast_type_map.get(node_type, f'NETLIST_{node_type}')
        
        # Print node
        if len(input_signals) > 0:
            print(f"{indent}{ast_type} <{node_id}>")
            
            # Print children (inputs)
            for input_signal in input_signals:
                # Check if this signal is output of another node (including temp signals)
                if input_signal in signal_to_node:
                    # This is output of another node - recursive print
                    child_node = signal_to_node[input_signal]
                    self._print_expression_tree(
                        child_node, all_nodes, signal_to_node,
                        node_by_id, node_outputs, all_signals,
                        indent=indent + "  "
                    )
                elif input_signal in all_signals:
                    # Valid signal (input or intermediate) - print as identifier
                    if input_signal in ['const_True', 'const_False', '1', '0']:
                        const_val = '1' if input_signal in ['const_True', '1'] else '0'
                        print(f"{indent}  NETLIST_CONSTANT <{const_val}>")
                    else:
                        print(f"{indent}  NETLIST_IDENTIFIER <{input_signal}>")
                else:
                    # Unknown signal - print as-is
                    print(f"{indent}  NETLIST_IDENTIFIER <{input_signal}>")
        else:
            # Leaf node
            if node_type in ['CONST0', 'CONST1']:
                const_val = '1' if node_type == 'CONST1' else '0'
                print(f"{indent}NETLIST_CONSTANT <{const_val}>")
            else:
                print(f"{indent}{ast_type} <{node_id}>")
    
    def _export_synthesized_json(self):
        """Tự động export JSON sau synthesis."""
        if not self.current_netlist:
            return
        
        try:
            import os
            if hasattr(self, 'filename') and self.filename:
                base_name = os.path.splitext(os.path.basename(self.filename))[0]
                output_dir = "outputs"
                if os.path.exists(output_dir):
                    filename = os.path.join(output_dir, f"{base_name}_synthesized.json")
                else:
                    filename = f"{base_name}_synthesized.json"
            else:
                filename = "netlist_synthesized.json"
            
            import json
            from datetime import datetime
            
            # Tạo bản copy và cập nhật metadata
            export_netlist = json.loads(json.dumps(self.current_netlist))
            export_netlist = self._update_metadata_stats(export_netlist)
            
            export_data = {
                "metadata": {
                    "tool": "MyLogic EDA Tool v2.0.0",
                    "export_time": datetime.now().isoformat(),
                    "source_file": getattr(self, 'filename', 'unknown'),
                    "version": "2.0.0",
                    "synthesis_level": level,
                    "auto_exported": True
                },
                "netlist": export_netlist
            }
            
            # Đảm bảo thư mục outputs tồn tại
            output_dir = os.path.dirname(filename) if os.path.dirname(filename) else "."
            if output_dir == "outputs" and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            # Đếm nodes chính xác để hiển thị
            nodes = export_netlist.get('nodes', [])
            node_count = len(nodes) if isinstance(nodes, (dict, list)) else 0
            print(f"[INFO] Auto-exported synthesized netlist to: {filename} ({node_count} nodes)")
            
        except Exception as e:
            # Không in lỗi để không làm gián đoạn flow
            pass
    
    def _auto_export_json(self):
        """Tự động export JSON sau khi đọc file (internal use)."""
        if not self.current_netlist:
            return
        
        # Tạo tên file JSON từ tên file Verilog
        if hasattr(self, 'filename') and self.filename:
            import os
            base_name = os.path.splitext(os.path.basename(self.filename))[0]
            # Export vào thư mục outputs nếu có, không thì cùng thư mục
            output_dir = "outputs"
            if os.path.exists(output_dir):
                filename = os.path.join(output_dir, f"{base_name}_parsed.json")
            else:
                filename = f"{base_name}_parsed.json"
        else:
            filename = "netlist_parsed.json"
        
        try:
            import json
            from datetime import datetime
            
            # Tạo bản copy để không sửa netlist gốc
            export_netlist = json.loads(json.dumps(self.current_netlist))
            
            # Cập nhật metadata stats
            export_netlist = self._update_metadata_stats(export_netlist)
            
            # Prepare export data
            export_data = {
                "metadata": {
                    "tool": "MyLogic EDA Tool v2.0.0",
                    "export_time": datetime.now().isoformat(),
                    "source_file": getattr(self, 'filename', 'unknown'),
                    "version": "2.0.0",
                    "auto_exported": True
                },
                "netlist": export_netlist
            }
            
            # Đảm bảo thư mục outputs tồn tại
            import os
            output_dir = os.path.dirname(filename) if os.path.dirname(filename) else "."
            if output_dir == "outputs" and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # Write JSON file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"[INFO] Auto-exported JSON to: {filename}")
            
        except Exception as e:
            # Không in lỗi khi auto-export để không làm gián đoạn flow
            pass
    
    def _update_metadata_stats(self, netlist):
        """Cập nhật parsing_stats và operator_summary sau synthesis."""
        if not netlist or 'nodes' not in netlist:
            return netlist
        
        nodes = netlist.get('nodes', [])
        if isinstance(nodes, dict):
            nodes_list = list(nodes.values())
        elif isinstance(nodes, list):
            nodes_list = nodes
        else:
            return netlist
        
        # Đếm số nodes theo type
        type_counts = {}
        category_counts = {
            'logic': 0,
            'arith': 0,
            'shift': 0,
            'compare': 0,
            'logical': 0,
            'struct': 0,
            'sequential': 0
        }
        
        for node in nodes_list:
            if isinstance(node, dict):
                node_type = node.get('type', 'UNKNOWN')
                type_counts[node_type] = type_counts.get(node_type, 0) + 1
                
                # Phân loại node
                if node_type in ['AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR', 'NOT', 'BUF']:
                    category_counts['logic'] += 1
                elif node_type in ['ADD', 'SUB', 'MUL', 'DIV', 'MOD']:
                    category_counts['arith'] += 1
                elif node_type in ['SHL', 'SHR', 'ASHL', 'ASHR']:
                    category_counts['shift'] += 1
                elif node_type in ['EQ', 'NE', 'LT', 'LE', 'GT', 'GE']:
                    category_counts['compare'] += 1
                elif node_type in ['ANDL', 'ORL', 'NOTL']:
                    category_counts['logical'] += 1
                elif node_type in ['DFF', 'LATCH']:
                    category_counts['sequential'] += 1
        
        # Cập nhật attrs nếu chưa có
        if 'attrs' not in netlist:
            netlist['attrs'] = {}
        
        # Cập nhật operator_summary
        netlist['attrs']['operator_summary'] = {
            'type_counts': type_counts,
            'category_counts': category_counts,
            'total_nodes': len(nodes_list)
        }
        
        # Cập nhật parsing_stats
        stats = netlist['attrs'].setdefault('parsing_stats', {})
        stats.update({
            'total_nodes': len(nodes_list),
            'logic_nodes': category_counts['logic'],
            'arith_nodes': category_counts['arith'],
            'shift_nodes': category_counts['shift'],
            'compare_nodes': category_counts['compare'],
            'logical_nodes': category_counts['logical'],
            'struct_nodes': category_counts['struct']
        })
        
        return netlist
    
    def _export_json(self, parts=None):
        """Export netlist to JSON file."""
        if not self.current_netlist:
            print("No netlist loaded. Use 'read <file>' first.")
            return
        
        # Get filename from command or use default
        if parts and len(parts) > 1:
            filename = parts[1]
            if not filename.endswith('.json'):
                filename += '.json'
        else:
            # Use current filename with .json extension
            if hasattr(self, 'filename') and self.filename:
                base_name = self.filename.replace('.v', '').replace('.logic', '')
                filename = f"{base_name}_netlist.json"
            else:
                filename = "netlist.json"
        
        try:
            import json
            from datetime import datetime
            
            # Tạo bản copy để không sửa netlist gốc
            export_netlist = json.loads(json.dumps(self.current_netlist))
            
            # Cập nhật metadata stats trước khi export
            export_netlist = self._update_metadata_stats(export_netlist)
            
            # Đếm nodes chính xác
            nodes = export_netlist.get('nodes', [])
            if isinstance(nodes, dict):
                node_count = len(nodes)
            elif isinstance(nodes, list):
                node_count = len(nodes)
            else:
                node_count = 0
            
            # Prepare export data
            export_data = {
                "metadata": {
                    "tool": "MyLogic EDA Tool v2.0.0",
                    "export_time": datetime.now().isoformat(),
                    "source_file": getattr(self, 'filename', 'unknown'),
                    "version": "2.0.0",
                    "auto_exported": False
                },
                "netlist": export_netlist
            }
            
            # Write JSON file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"[OK] Successfully exported netlist to: {filename}")
            print(f"[INFO] File contains:")
            print(f"   - {node_count} nodes")
            print(f"   - {len(export_netlist.get('wires', []))} wires")
            print(f"   - {len(export_netlist.get('inputs', []))} inputs")
            print(f"   - {len(export_netlist.get('outputs', []))} outputs")
            
        except Exception as e:
            print(f"[ERROR] Error exporting JSON: {e}")
    
    def _run_aig(self, parts):
        """Chạy AIG (And-Inverter Graph) operations."""
        if not parts or len(parts) < 2:
            print("Usage: aig <operation>")
            print("Operations: create, strash, convert, stats")
            return
        
        operation = parts[1].lower()
        
        try:
            from core.synthesis.aig import AIG
            
            if operation == "create":
                self._aig_create_example()
            elif operation == "strash":
                self._aig_strash_example()
            elif operation == "convert":
                self._aig_convert_to_verilog()
            elif operation == "stats":
                self._aig_statistics()
            else:
                print("Invalid AIG operation. Use: create, strash, convert, or stats")
                
        except ImportError:
            print("[ERROR] AIG module not available")
        except Exception as e:
            print(f"[ERROR] AIG operation failed: {e}")
    
    def _aig_create_example(self):
        """Minh họa AIG creation."""
        from core.synthesis.aig import AIG
        
        aig = AIG()
        a = aig.create_pi("a")
        b = aig.create_pi("b")
        c = aig.create_pi("c")
        
        # Create logic: f = (a AND b) OR c
        ab = aig.create_and(a, b)
        f = aig.create_or(ab, c)
        aig.add_po(f)
        
        print("AIG Creation Example:")
        print(f"  Expression: (a AND b) OR c")
        stats = aig.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    def _aig_strash_example(self):
        """Minh họa AIG structural hashing."""
        from core.synthesis.aig import AIG
        
        aig = AIG()
        a = aig.create_pi("a")
        b = aig.create_pi("b")
        
        # Create duplicate AND nodes
        ab1 = aig.create_and(a, b)
        ab2 = aig.create_and(a, b)  # Should reuse ab1
        
        print("AIG Structural Hashing Example:")
        print(f"  ab1 node_id: {ab1.node_id}")
        print(f"  ab2 node_id: {ab2.node_id}")
        print(f"  Same node (structural hashing): {ab1 == ab2}")
        print(f"  Total nodes: {aig.count_nodes()}")
    
    def _aig_convert_to_verilog(self):
        """Convert AIG to Verilog."""
        from core.synthesis.aig import AIG
        
        aig = AIG()
        a = aig.create_pi("a")
        b = aig.create_pi("b")
        c = aig.create_pi("c")
        
        ab = aig.create_and(a, b)
        f = aig.create_or(ab, c)
        aig.add_po(f)
        
        print("AIG to Verilog Conversion:")
        verilog = aig.to_verilog("example_aig")
        print(verilog)
    
    def _aig_statistics(self):
        """Show AIG statistics."""
        from core.synthesis.aig import AIG
        
        aig = AIG()
        a = aig.create_pi("a")
        b = aig.create_pi("b")
        c = aig.create_pi("c")
        
        ab = aig.create_and(a, b)
        ac = aig.create_and(a, c)
        f = aig.create_or(ab, ac)
        aig.add_po(f)
        
        print("AIG Statistics:")
        stats = aig.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")


def main():
    """Main entry point cho vector shell."""
    import argparse
    
    parser = argparse.ArgumentParser(description="MyLogic Vector Shell")
    parser.add_argument("--file", "-f", help="Verilog file to load")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Tạo shell
    shell = MyLogicShell()
    
    # Load file nếu được chỉ định
    if args.file:
        shell._read_file(["read", args.file])
    
    # Chạy shell
    shell.run()


if __name__ == "__main__":
    main()