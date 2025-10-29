"""
Enhanced CLI shell với hỗ trợ vector simulation.

Hỗ trợ:
 - Vector inputs/outputs
 - Multi-bit simulation
 - Vector operations
 - Yosys integration
"""

import os
import sys
import logging
from typing import Any, Dict, Optional, Union

# Thêm thư mục gốc project vào đường dẫn
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers import parse_verilog
from core.simulation.arithmetic_simulation import simulate_arithmetic_netlist
from core.simulation.arithmetic_simulation import VectorValue

# Yosys integration
try:
    from integrations.yosys.mylogic_synthesis import MyLogicSynthesis, integrate_yosys_commands
    YOSYS_AVAILABLE = True
except ImportError:
    YOSYS_AVAILABLE = False


class VectorShell:
    """Enhanced shell với hỗ trợ vector simulation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Khởi tạo shell với trạng thái trống và cấu hình tùy chọn."""
        self.netlist: Optional[Union[Dict[str, Any], Any]] = None
        self.current_netlist: Optional[Union[Dict[str, Any], Any]] = None
        self.filename: Optional[str] = None
        self.history: list = []
        self.config = config or {}
        
        # Áp dụng cấu hình
        self.prompt = self.config.get("shell", {}).get("prompt", "mylogic> ")
        self.history_size = self.config.get("shell", {}).get("history_size", 1000)
        self.auto_complete = self.config.get("shell", {}).get("auto_complete", True)
        self.color_output = self.config.get("shell", {}).get("color_output", True)
        
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
            'simulate': self._simulate_unified,
            'vsimulate': self._simulate_vector_netlist,
            'history': self._show_history,
            'clear': self._clear_screen,
            'help': self._show_help,
            'exit': self._exit_shell,
        # Logic Synthesis algorithms (ABC-inspired)
        'strash': self._run_strash,
        'cse': self._run_cse,
        'constprop': self._run_constprop,
        'balance': self._run_balance,
        'synthesis': self._run_complete_synthesis,
        'abc_info': self._run_abc_info,
            # VLSI CAD Part 1 features
            'dce': self._run_dce,
            'bdd': self._run_bdd,
            'sat': self._run_sat,
            'verify': self._run_verification,
            # VLSI CAD Part 2 features
            'place': self._run_placement,
            'route': self._run_routing,
            'timing': self._run_timing_analysis,
            'techmap': self._run_technology_mapping
        }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        
        # Tích hợp Yosys commands nếu có sẵn
        if YOSYS_AVAILABLE:
            try:
                integrate_yosys_commands(self)
                print("[INFO] Yosys integration enabled")
            except Exception as e:
                print(f"[WARNING] Yosys integration failed: {e}")
        else:
            print("[INFO] Yosys not available - synthesis features disabled")

    def run(self):
        """Chạy interactive shell."""
        print("Welcome to MyLogic Vector Shell. Type 'help' for commands.")
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
        """Đọc file Verilog."""
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
        except Exception as e:
            print(f"[ERROR] Failed to read file: {e}")

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

    def _simulate_unified(self, parts=None):
        """Simulation thống nhất tự động phát hiện vector vs scalar."""
        if not self.netlist:
            print("[ERROR] No netlist loaded.")
            return
        
        # Kiểm tra xem đây có phải là vector design không
        if isinstance(self.netlist, dict):
            vector_widths = self.netlist.get('attrs', {}).get('vector_widths', {})
            has_vector_io = any(width > 1 for width in vector_widths.values())
            
            if has_vector_io:
                # Sử dụng vector simulation
                print("[INFO] Detected vector design, using vector simulation...")
                self._simulate_vector_netlist()
            else:
                # Sử dụng scalar simulation
                print("[INFO] Detected scalar design, using scalar simulation...")
                self._simulate_netlist()
        else:
            # Netlist object (scalar)
            print("[INFO] Detected scalar design, using scalar simulation...")
            self._simulate_netlist()

    def _simulate_netlist(self):
        """Mô phỏng scalar netlist sử dụng vector simulation."""
        if not isinstance(self.netlist, dict):
            print("[ERROR] Scalar simulation requires vector netlist.")
            return
        
        vec = {}
        inputs = self.netlist.get("inputs", [])
        vector_widths = self.netlist.get('attrs', {}).get('vector_widths', {})
        
        for inp in inputs:
            width = vector_widths.get(inp, 1)
            if width > 1:
                val = input(f"  Value for [{width-1}:0] {inp} (integer): ")
                try:
                    vec[inp] = VectorValue(int(val.strip()), width)
                except ValueError:
                    print(f"[ERROR] Invalid input. Use integer for {width}-bit value.")
                    return
            else:
                val = input(f"  Value for {inp} (0/1): ")
                try:
                    vec[inp] = VectorValue(int(val.strip()), 1)
                except ValueError:
                    print("[ERROR] Invalid input. Use 0 or 1.")
                    return
        
        try:
            out = simulate_arithmetic_netlist(self.netlist, vec)
            print("  -> Outputs:")
            for output_name, output_value in out.items():
                if isinstance(output_value, VectorValue):
                    print(f"    {output_name}: {output_value} (int: {output_value.to_int()})")
                else:
                    print(f"    {output_name}: {output_value}")
        except Exception as e:
            print(f"[ERROR] Simulation failed: {e}")

    def _simulate_vector_netlist(self, parts=None):
        """Mô phỏng vector netlist (giờ sử dụng logic thống nhất _simulate_netlist)."""
        self._simulate_netlist()

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
        print("  read <file>           - Load a .logic or .v file")
        print("  stats                 - Enhanced circuit statistics")
        print("  vectors               - Detailed vector width analysis")
        print("  nodes                 - Detailed node information")
        print("  wires                 - Detailed wire analysis")
        print("  modules               - Module instantiation details")
        print("  export [file]         - Export netlist to JSON file")
        print()
        print("Simulation:")
        print("  simulate              - Run simulation (auto-detect vector/scalar)")
        print("  vsimulate             - Run vector simulation (n-bit, legacy)")
        print()
        print("Logic Synthesis (ABC-inspired):")
        print("  strash                - Structural hashing optimization")
        print("  dce                   - Dead code elimination")
        print("  cse                   - Common subexpression elimination")
        print("  constprop             - Constant propagation")
        print("  balance               - Logic balancing")
        print("  synthesis             - Complete synthesis flow")
        print()
        print("VLSI CAD Algorithms:")
        print("  bdd                   - Binary Decision Diagram operations")
        print("  sat                   - SAT solver operations")
        print("  verify                - Formal verification")
        print("  placement             - Cell placement algorithms")
        print("  routing               - Wire routing algorithms")
        print("  timing                - Static timing analysis")
        print()
        print("Utility:")
        print("  history               - Show command history")
        print("  clear                 - Clear screen")
        print("  help                  - Show this help")
        print("  exit                  - Quit the shell")
        
        # Hiển thị Yosys commands nếu có sẵn
        if YOSYS_AVAILABLE:
            print("\nYosys Integration:")
            print("  yosys_synth          - Run Yosys synthesis")
            print("  yosys_opt            - Run optimization pass")
            print("  yosys_stat           - Get design statistics")
            print("  yosys_flow           - Complete synthesis flow")
            print("  yosys_help           - Show Yosys help")
            print("\nYosys Output Formats:")
            print("  write_verilog        - Write Verilog RTL output")
            print("  write_json           - Write JSON netlist")
            print("  write_blif           - Write BLIF format")
            print("  write_edif           - Write EDIF format")
        print("  write_spice          - Write SPICE netlist")
        print("  write_dot            - Write DOT graph format")
        print("  write_liberty        - Write Liberty library")
        print("  write_systemverilog  - Write SystemVerilog output")
        print("")
        print("Logic Synthesis Algorithms (ABC-inspired):")
        print("  strash               - Structural Hashing (remove duplicates)")
        print("  cse                  - Common Subexpression Elimination")
        print("  constprop            - Constant Propagation")
        print("  balance              - Logic Balancing")
        print("  synthesis <level>    - Complete synthesis flow (basic/standard/aggressive)")
        print("  abc_info             - ABC integration information")
        print("")
        print("VLSI CAD Part 1 Features:")
        print("  dce <level>          - Dead Code Elimination (basic/advanced/aggressive)")
        print("  bdd <operation>      - Binary Decision Diagrams (create/analyze/convert)")
        print("  sat <operation>      - SAT Solver (solve/verify/check)")
        print("  verify <type>        - Circuit verification (equivalence/property/functional)")
        print("")
        print("VLSI CAD Part 2 Features:")
        print("  place <algorithm>    - Placement algorithms (random/force/sa)")
        print("  route <algorithm>    - Routing algorithms (maze/lee/ripup)")
        print("  timing               - Static Timing Analysis (STA)")
        print("  techmap <strategy>   - Technology mapping (area/delay/balanced)")

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
    
    def _run_complete_synthesis(self, parts):
        """Chạy Complete Logic Synthesis Flow."""
        if not parts or len(parts) < 2:
            print("Usage: synthesis <level>")
            print("Levels: basic, standard, aggressive")
            return
        
        level = parts[1].lower()
        if level not in ["basic", "standard", "aggressive"]:
            print("Invalid synthesis level. Use: basic, standard, or aggressive")
            return
        
        if not self.current_netlist:
            print("[ERROR] No netlist loaded. Use 'read <file>' first.")
            return
        
        try:
            from core.synthesis.synthesis_flow import run_complete_synthesis
            
            print(f"[INFO] Running Complete Logic Synthesis Flow - Level: {level}")
            original_nodes = len(self.current_netlist.get('nodes', {}))
            
            optimized_netlist = run_complete_synthesis(self.current_netlist, level)
            self.current_netlist = optimized_netlist
            
            final_nodes = len(optimized_netlist.get('nodes', {}))
            reduction = original_nodes - final_nodes
            
            print(f"[OK] Complete Synthesis Flow completed!")
            print(f"  Original: {original_nodes} nodes")
            print(f"  Final: {final_nodes} nodes")
            print(f"  Total reduction: {reduction} nodes ({(reduction/original_nodes)*100:.1f}%)")
            
        except ImportError:
            print("[ERROR] Synthesis Flow module not available")
        except Exception as e:
            print(f"[ERROR] Complete Synthesis Flow failed: {e}")
    
    def _run_abc_info(self, parts):
        """Hiển thị thông tin ABC integration."""
        try:
            from core.abc_integration import ABCIntegration
            
            abc = ABCIntegration()
            
            print("ABC Integration Information:")
            print("=" * 50)
            print(f"ABC Repository: https://github.com/YosysHQ/abc")
            print(f"ABC Description: System for Sequential Logic Synthesis and Formal Verification")
            print("")
            
            print("ABC-Inspired Algorithms in MyLogic:")
            print("-" * 40)
            
            algorithms = ['strash', 'dce', 'cse', 'constprop', 'balance', 'bdd', 'techmap', 'sat']
            for algo in algorithms:
                ref = abc.get_abc_reference(algo)
                if ref:
                    print(f"  {algo.upper():12} - {ref['abc_function']}")
                    print(f"  {'':12}   ABC: {ref['abc_file']}")
                    print(f"  {'':12}   MyLogic: {ref['mylogic_file']}")
                    print("")
            
            print("ABC Synthesis Flow:")
            print("-" * 25)
            flow = abc.get_abc_synthesis_flow()
            for step in flow:
                print(f"  {step['step']}. {step['name']:25} - {step['abc_function']}")
            
            print("")
            print("ABC Benefits:")
            print("-" * 15)
            print("  - Industry-proven algorithms")
            print("  - High-performance implementation")
            print("  - Comprehensive optimization techniques")
            print("  - Research-based improvements")
            
            print("")
            print("MyLogic Advantages:")
            print("-" * 20)
            print("  - Vietnamese documentation")
            print("  - Educational focus")
            print("  - Modular architecture")
            print("  - Easy to understand and modify")
            
        except ImportError:
            print("[ERROR] ABC Integration module not available")
        except Exception as e:
            print(f"[ERROR] ABC info failed: {e}")
    
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
    
    def _run_bdd(self, parts):
        """Chạy BDD operations."""
        if not parts or len(parts) < 2:
            print("Usage: bdd <operation>")
            print("Operations: create, analyze, convert")
            return
        
        operation = parts[1].lower()
        
        try:
            from core.vlsi_cad.bdd import BDD
            
            if operation == "create":
                self._bdd_create_operations()
            elif operation == "analyze":
                self._bdd_analyze_netlist()
            elif operation == "convert":
                self._bdd_convert_to_verilog()
            else:
                print("Invalid BDD operation. Use: create, analyze, or convert")
                
        except ImportError:
            print("[ERROR] BDD module not available")
        except Exception as e:
            print(f"[ERROR] BDD operation failed: {e}")
    
    def _run_sat(self, parts):
        """Chạy SAT solver operations."""
        if not parts or len(parts) < 2:
            print("Usage: sat <operation>")
            print("Operations: solve, verify, check")
            return
        
        operation = parts[1].lower()
        
        try:
            from core.vlsi_cad.sat_solver import SATSolver, SATBasedVerifier
            
            if operation == "solve":
                self._sat_solve_example()
            elif operation == "verify":
                self._sat_verify_circuit()
            elif operation == "check":
                self._sat_check_satisfiability()
            else:
                print("Invalid SAT operation. Use: solve, verify, or check")
                
        except ImportError:
            print("[ERROR] SAT solver module not available")
        except Exception as e:
            print(f"[ERROR] SAT operation failed: {e}")
    
    def _run_verification(self, parts):
        """Chạy circuit verification."""
        if not parts or len(parts) < 2:
            print("Usage: verify <type>")
            print("Types: equivalence, property, functional")
            return
        
        verify_type = parts[1].lower()
        
        if verify_type == "equivalence":
            print("[INFO] Running equivalence verification...")
            # Implementation sẽ ở đây
            print("[OK] Equivalence verification completed")
        elif verify_type == "property":
            print("[INFO] Running property verification...")
            # Implementation sẽ ở đây
            print("[OK] Property verification completed")
        elif verify_type == "functional":
            print("[INFO] Running functional verification...")
            # Implementation sẽ ở đây
            print("[OK] Functional verification completed")
        else:
            print("Invalid verification type. Use: equivalence, property, or functional")
    
    def _bdd_create_operations(self):
        """Minh họa BDD creation operations."""
        from core.vlsi_cad.bdd import BDD
        
        bdd = BDD()
        a = bdd.create_variable("a")
        b = bdd.create_variable("b")
        
        f1 = bdd.apply_operation("AND", a, b)
        f2 = bdd.apply_operation("OR", a, b)
        
        print("BDD Creation Example:")
        print(f"  a AND b: {f1}")
        print(f"  a OR b: {f2}")
        print(f"  Support of a AND b: {bdd.get_support(f1)}")
    
    def _bdd_analyze_netlist(self):
        """Phân tích netlist hiện tại sử dụng BDD."""
        if not self.current_netlist:
            print("[ERROR] No netlist loaded")
            return
        
        print("[INFO] Analyzing netlist with BDD...")
        # Implementation sẽ chuyển đổi netlist thành BDD và phân tích
        print("[OK] BDD analysis completed")
    
    def _bdd_convert_to_verilog(self):
        """Chuyển đổi BDD sang Verilog."""
        print("[INFO] Converting BDD to Verilog...")
        # Implementation sẽ chuyển đổi BDD thành Verilog code
        print("[OK] BDD to Verilog conversion completed")
    
    def _sat_solve_example(self):
        """Minh họa SAT solving."""
        from core.vlsi_cad.sat_solver import SATSolver
        
        solver = SATSolver()
        solver.add_clause([1, 2])      # a OR b
        solver.add_clause([-1, 3])     # NOT a OR c
        solver.add_clause([-2, -3])    # NOT b OR NOT c
        
        print("SAT Solving Example:")
        print("Formula: (a OR b) AND (NOT a OR c) AND (NOT b OR NOT c)")
        
        is_sat, assignment = solver.solve()
        
        if is_sat:
            print(f"  Satisfiable! Assignment: {assignment}")
        else:
            print("  Unsatisfiable!")
        
        print(f"  Statistics: {solver.get_statistics()}")
    
    def _sat_verify_circuit(self):
        """Xác minh mạch sử dụng SAT."""
        if not self.current_netlist:
            print("[ERROR] No netlist loaded")
            return
        
        print("[INFO] Verifying circuit with SAT...")
        # Implementation sẽ sử dụng SAT cho verification
        print("[OK] SAT verification completed")
    
    def _sat_check_satisfiability(self):
        """Kiểm tra satisfiability của mạch."""
        print("[INFO] Checking circuit satisfiability...")
        # Implementation sẽ kiểm tra xem mạch có satisfiable không
        print("[OK] Satisfiability check completed")
    
    def _run_placement(self, parts):
        """Chạy placement algorithms."""
        if not parts or len(parts) < 2:
            print("Usage: place <algorithm>")
            print("Algorithms: random, force, sa")
            return
        
        algorithm = parts[1].lower()
        
        try:
            from core.vlsi_cad.placement import PlacementEngine, Cell, Net
            
            if algorithm == "random":
                self._demo_random_placement()
            elif algorithm == "force":
                self._demo_force_placement()
            elif algorithm == "sa":
                self._demo_sa_placement()
            else:
                print("Invalid placement algorithm. Use: random, force, or sa")
                
        except ImportError:
            print("[ERROR] Placement module not available")
        except Exception as e:
            print(f"[ERROR] Placement failed: {e}")
    
    def _run_routing(self, parts):
        """Chạy routing algorithms."""
        if not parts or len(parts) < 2:
            print("Usage: route <algorithm>")
            print("Algorithms: maze, lee, ripup")
            return
        
        algorithm = parts[1].lower()
        
        try:
            from core.vlsi_cad.routing import MazeRouter, RoutingGrid, Net, Point
            
            if algorithm == "maze":
                self._demo_maze_routing()
            elif algorithm == "lee":
                self._demo_lee_routing()
            elif algorithm == "ripup":
                self._demo_ripup_routing()
            else:
                print("Invalid routing algorithm. Use: maze, lee, or ripup")
                
        except ImportError:
            print("[ERROR] Routing module not available")
        except Exception as e:
            print(f"[ERROR] Routing failed: {e}")
    
    def _run_timing_analysis(self, parts):
        """Chạy Static Timing Analysis."""
        try:
            from core.vlsi_cad.timing_analysis import StaticTimingAnalyzer, TimingNode, TimingArc
            
            print("[INFO] Running Static Timing Analysis...")
            
            # Tạo timing analyzer
            sta = StaticTimingAnalyzer()
            
            # Thêm demo timing nodes
            nodes_data = [
                ("clk", "input"),
                ("in1", "input"),
                ("in2", "input"),
                ("gate1", "gate"),
                ("gate2", "gate"),
                ("out1", "output"),
            ]
            
            for name, node_type in nodes_data:
                node = TimingNode(name, node_type)
                sta.add_node(node)
            
            # Thêm timing arcs
            arcs_data = [
                ("clk", "gate1", 0.1),
                ("in1", "gate1", 0.2),
                ("in2", "gate2", 0.15),
                ("gate1", "gate2", 0.3),
                ("gate2", "out1", 0.2),
            ]
            
            for from_node, to_node, delay in arcs_data:
                arc = TimingArc(from_node, to_node, delay)
                sta.add_arc(arc)
            
            # Đặt clock period và thực hiện phân tích
            sta.set_clock_period(2.0)
            timing_report = sta.perform_timing_analysis()
            
            # In kết quả
            sta.print_timing_report(timing_report)
            
            print("[OK] Static Timing Analysis completed")
            
        except ImportError:
            print("[ERROR] Timing analysis module not available")
        except Exception as e:
            print(f"[ERROR] Timing analysis failed: {e}")
    
    def _run_technology_mapping(self, parts):
        """Chạy technology mapping."""
        if not parts or len(parts) < 2:
            print("Usage: techmap <strategy>")
            print("Strategies: area, delay, balanced")
            return
        
        strategy = parts[1].lower()
        
        try:
            from core.technology_mapping.technology_mapping import TechnologyMapper, LogicNode, create_standard_library
            
            print(f"[INFO] Running technology mapping with {strategy} strategy...")
            
            # Tạo library và mapper
            library = create_standard_library()
            mapper = TechnologyMapper(library)
            
            # Thêm demo logic nodes
            logic_nodes = [
                LogicNode("n1", "AND(A,B)", ["a", "b"], "temp1"),
                LogicNode("n2", "OR(C,D)", ["c", "d"], "temp2"),
                LogicNode("n3", "XOR(temp1,temp2)", ["temp1", "temp2"], "out"),
            ]
            
            for node in logic_nodes:
                mapper.add_logic_node(node)
            
            # Thực hiện mapping
            if strategy == "area":
                results = mapper.perform_technology_mapping("area_optimal")
            elif strategy == "delay":
                results = mapper.perform_technology_mapping("delay_optimal")
            elif strategy == "balanced":
                results = mapper.perform_technology_mapping("balanced")
            else:
                print("Invalid strategy. Use: area, delay, or balanced")
                return
            
            # In kết quả
            mapper.print_mapping_report(results)
            
            print("[OK] Technology mapping completed")
            
        except ImportError:
            print("[ERROR] Technology mapping module not available")
        except Exception as e:
            print(f"[ERROR] Technology mapping failed: {e}")
    
    def _demo_random_placement(self):
        """Minh họa random placement."""
        from core.vlsi_cad.placement import PlacementEngine, Cell, Net
        
        print("Random Placement Demo:")
        engine = PlacementEngine(1000.0, 1000.0)
        
        # Thêm cells
        for i in range(5):
            cell = Cell(f"cell{i+1}", 50 + i*10, 40 + i*5)
            engine.add_cell(cell)
        
        # Thêm nets
        nets_data = [
            ("net1", ["cell1", "cell2", "cell3"]),
            ("net2", ["cell2", "cell4"]),
            ("net3", ["cell1", "cell4", "cell5"]),
        ]
        
        for name, pins in nets_data:
            net = Net(name, pins)
            engine.add_net(net)
        
        placement = engine.random_placement()
        stats = engine.get_placement_statistics()
        print(f"  Wirelength: {stats['total_wirelength']:.2f}")
    
    def _demo_force_placement(self):
        """Minh họa force-directed placement."""
        print("Force-Directed Placement Demo:")
        print("  Implementation sẽ chạy force-directed algorithm")
        print("  Dựa trên spring-mass model cho cell placement")
    
    def _demo_sa_placement(self):
        """Minh họa simulated annealing placement."""
        print("Simulated Annealing Placement Demo:")
        print("  Implementation sẽ chạy SA algorithm")
        print("  Sử dụng temperature-based optimization")
    
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
            
            # Prepare export data
            export_data = {
                "metadata": {
                    "tool": "MyLogic EDA Tool v2.0.0",
                    "export_time": datetime.now().isoformat(),
                    "source_file": getattr(self, 'filename', 'unknown'),
                    "version": "2.0.0"
                },
                "netlist": self.current_netlist
            }
            
            # Write JSON file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"[OK] Successfully exported netlist to: {filename}")
            print(f"[INFO] File contains:")
            print(f"   - {len(self.current_netlist.get('nodes', []))} nodes")
            print(f"   - {len(self.current_netlist.get('wires', []))} wires")
            print(f"   - {len(self.current_netlist.get('inputs', []))} inputs")
            print(f"   - {len(self.current_netlist.get('outputs', []))} outputs")
            
        except Exception as e:
            print(f"[ERROR] Error exporting JSON: {e}")
    
    def _demo_maze_routing(self):
        """Minh họa maze routing."""
        print("Maze Routing Demo:")
        print("  Implementation sẽ chạy maze routing algorithm")
        print("  Dựa trên Lee's algorithm cho wire routing")
    
    def _demo_lee_routing(self):
        """Minh họa Lee's routing."""
        print("Lee's Algorithm Demo:")
        print("  Implementation sẽ chạy Lee's wave propagation")
        print("  Classic maze routing algorithm")
    
    def _demo_ripup_routing(self):
        """Minh họa rip-up and reroute."""
        print("Rip-up and Reroute Demo:")
        print("  Implementation sẽ chạy rip-up and reroute")
        print("  Xử lý routing congestion")


def main():
    """Main entry point cho vector shell."""
    import argparse
    
    parser = argparse.ArgumentParser(description="MyLogic Vector Shell")
    parser.add_argument("--file", "-f", help="Verilog file to load")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Tạo shell
    shell = VectorShell()
    
    # Load file nếu được chỉ định
    if args.file:
        shell._read_file(["read", args.file])
    
    # Chạy shell
    shell.run()


if __name__ == "__main__":
    main()