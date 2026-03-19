import os
import sys
import logging
from typing import Any, Dict, Optional, Union

# Thêm thư mục gốc project vào đường dẫn
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.commands import dump_ast, file_ops, help_cmd, inspect, synthesis_cmds

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
        
        # Khởi tạo từ điển commands (đăng ký từ các modules)
        self.commands: Dict[str, Any] = {}
        self.commands.update(file_ops.register(self))
        self.commands.update(inspect.register(self))
        self.commands.update(dump_ast.register(self))
        self.commands.update(synthesis_cmds.register(self))
        self.commands.update(help_cmd.register(self))

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
                except SystemExit:
                    raise
                except Exception as e:
                    print(f"[ERROR] Command error: {e}")
            else:
                print(f"[ERROR] Unknown command: {op}")
                print("Type 'help' for available commands.")

    # ---------------------------------------------------------------------
    # Backward-compatibility shims (old method names)
    # These delegate to the new command handlers registered in self.commands.
    # ---------------------------------------------------------------------

    def _show_stats(self, parts=None):
        return self.commands["stats"](parts)

    def _show_vector_details(self, parts=None):
        return self.commands["vectors"](parts)

    def _show_node_details(self, parts=None):
        return self.commands["nodes"](parts)

    def _show_wire_details(self, parts=None):
        return self.commands["wires"](parts)

    def _show_module_details(self, parts=None):
        return self.commands["modules"](parts)

    def _show_history(self, parts=None):
        return self.commands["history"](parts)

    def _clear_screen(self, parts=None):
        return self.commands["clear"](parts)

    def _show_help(self, parts=None):
        return self.commands["help"](parts)

    def _exit_shell(self, parts=None):
        return self.commands["exit"](parts)

    def _dump_ast(self, parts=None):
        return self.commands["dump"](parts)

    def _export_json(self, parts=None):
        return self.commands["export"](parts)

    def _run_synthesis(self, parts):
        return self.commands["synthesis"](parts)

    def _run_optimization(self, parts=None):
        return self.commands["optimize"](parts)

    def _run_strash(self, parts=None):
        return self.commands["strash"](parts)

    def _run_cse(self, parts=None):
        return self.commands["cse"](parts)

    def _run_constprop(self, parts=None):
        return self.commands["constprop"](parts)

    def _run_balance(self, parts=None):
        return self.commands["balance"](parts)

    def _run_dce(self, parts):
        return self.commands["dce"](parts)

    def _run_aig(self, parts):
        return self.commands["aig"](parts)

    def _run_technology_mapping(self, parts):
        return self.commands["techmap"](parts)

    def _run_complete_flow(self, parts):
        return self.commands["complete_flow"](parts)

    # (handlers moved to cli/commands/*)
    
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