#!/usr/bin/env python3
"""
MyLogic - Unified EDA Tool

Công cụ Tự động Hóa Thiết kế Điện tử (EDA) toàn diện cho thiết kế mạch số,
tối ưu hóa và xác minh với hỗ trợ cả scalar và vector.

Tính năng:
- Nhiều parser frontend (Verilog, Simple Language)
- Hỗ trợ mô phỏng Scalar và Vector
- Các bước tối ưu hóa nâng cao (Strash, DCE, CSE, ConstProp, Balance)
- Ánh xạ công nghệ (LUT-based, Liberty-based)
- Phân tích chi phí và tối ưu hóa
- Kiểm tra tương đương tổ hợp
- Shell CLI tương tác
- Phát hiện file thông minh

Cách sử dụng:
    python mylogic.py                    # Khởi động shell tương tác (tự động phát hiện)
    python mylogic.py --scalar           # Bắt buộc shell scalar
    python mylogic.py --vector           # Bắt buộc shell vector
    python mylogic.py --file <file>      # Load file và tự động phát hiện mode
    python mylogic.py --help             # Hiển thị help
    python mylogic.py --version          # Hiển thị phiên bản
"""

import sys
import os
import argparse
import json
import logging
import subprocess
from typing import Optional, Dict, Any

# Thêm thư mục gốc project vào đường dẫn để import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.vector_shell import VectorShell
from parsers import parse_verilog

# Import constants
from constants import (
    PROJECT_VERSION as VERSION,
    PROJECT_AUTHOR as AUTHOR, 
    PROJECT_DESCRIPTION_LONG as DESCRIPTION,
    WELCOME_MESSAGE,
    SUBTITLE_MESSAGE,
    FEATURES_MESSAGE
)

def setup_logging(debug: bool = False, log_file: Optional[str] = None) -> None:
    """Thiết lập cấu hình logging."""
    level = logging.DEBUG if debug else logging.INFO
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Ensure console uses UTF-8 to avoid UnicodeEncodeError on Windows
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

    # Stream handler with UTF-8 encoding for Windows consoles
    stream_handler = logging.StreamHandler(sys.stdout)
    try:
        stream_handler.setStream(open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1))
    except Exception:
        # Fallback quietly if not supported
        pass
    handlers = [stream_handler]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=handlers
    )
    
    # Giảm độ chi tiết của một số modules
    logging.getLogger('urllib3').setLevel(logging.WARNING)

def load_config(config_path: str = "config/mylogic_config.json") -> Dict[str, Any]:
    """Load cấu hình từ file JSON."""
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config
        else:
            return {}
    except Exception as e:
        print(f"[ERROR] Failed to load configuration: {e}")
        return {}

def detect_file_type(file_path: str) -> str:
    """Detect if file contains vector declarations."""
    if not os.path.exists(file_path):
        return "unknown"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for vector declarations
        if '[3:0]' in content or '[2:0]' in content or '[1:0]' in content or '[4:0]' in content:
            return "vector"
        else:
            return "scalar"
    except:
        return "unknown"

def run_synthesis_mode(file_path: str, level: str, debug: bool = False):
    """Chạy synthesis mode và thoát."""
    print("=" * 70)
    print(" MyLogic - Automatic Synthesis Mode")
    print("=" * 70)
    print(f"Input file: {file_path}")
    print(f"Optimization level: {level}")
    print("")
    
    try:
        # Parse Verilog
        print("[1/3] Parsing Verilog...")
        netlist = parse_verilog(file_path)
        original_nodes = len(netlist.get('nodes', {}))
        print(f"  Loaded {original_nodes} nodes")
        
        # Run synthesis
        print(f"\n[2/3] Running complete synthesis flow ({level})...")
        from core.synthesis.synthesis_flow import run_complete_synthesis
        synthesized = run_complete_synthesis(netlist, level)
        final_nodes = len(synthesized.get('nodes', {}))
        
        # Export results
        print("\n[3/3] Exporting results...")
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = os.path.join(output_dir, f"{base_name}_synthesized_{level}.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(synthesized, f, indent=2)
        
        print(f"  Exported to: {output_file}")
        
        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Original nodes: {original_nodes}")
        print(f"Optimized nodes: {final_nodes}")
        print(f"Reduction: {original_nodes - final_nodes} nodes ({((original_nodes-final_nodes)/original_nodes)*100:.1f}%)")
        print("=" * 70)
        print("[SUCCESS] Synthesis completed!")
        
    except Exception as e:
        print(f"\n[ERROR] Synthesis failed: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def check_dependencies():
    """Kiểm tra các dependencies cần thiết."""
    print("Checking dependencies...")
    
    # Kiểm tra NumPy
    try:
        import numpy
        print("[OK] NumPy is available")
    except ImportError:
        print("[WARNING] NumPy not available - some features may be limited")
    
    # Kiểm tra Matplotlib
    try:
        import matplotlib
        print("[OK] Matplotlib is available")
    except ImportError:
        print("[WARNING] Matplotlib not available - plotting features disabled")
    
    # Kiểm tra Graphviz
    try:
        result = subprocess.run(["dot", "-V"], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] Graphviz is available")
        else:
            print("[WARNING] Graphviz not available - DOT output disabled")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("[WARNING] Graphviz not available - DOT output disabled")

def create_shell(mode: str, config: Dict[str, Any], file_path: Optional[str] = None):
    """Create appropriate shell based on mode."""
    shell = VectorShell(config)
    print("=" * 60)
    print(WELCOME_MESSAGE)
    print(SUBTITLE_MESSAGE)
    print(FEATURES_MESSAGE)
    print("=" * 60)
    
    # Auto-load file if provided
    if file_path:
        try:
            netlist = parse_verilog(file_path)
            shell.netlist = netlist
            shell.current_netlist = netlist  # Also set current_netlist for optimization commands
            shell.filename = file_path
            print(f"[OK] Loaded vector netlist: {file_path}")
        except Exception as e:
            print(f"[ERROR] Failed to load file: {e}")
            print("[INFO] Starting shell without file")
    
    return shell

def show_usage_info(mode: str):
    """Show usage information based on mode."""
    print("\nUsage:")
    if mode == "vector":
        print("  vsimulate  - Vector simulation (n-bit)")
        print("  simulate   - Scalar simulation (1-bit, fallback)")
    else:
        print("  simulate   - Scalar simulation (1-bit)")
        print("  strash     - Structural hashing")
        print("  dce        - Dead code elimination")
        print("  cse        - Common subexpression elimination")
        print("  constprop  - Constant propagation")
        print("  balance    - Balance multi-input gates")
    print("  stats      - Show circuit statistics")
    print("  help       - Show all commands")
    print("  exit       - Quit shell")

def main():
    """Main entry point for MyLogic EDA Tool."""
    parser = argparse.ArgumentParser(
        description=f"{DESCRIPTION} v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mylogic.py                    # Start interactive shell (auto-detect)
  python mylogic.py --scalar           # Force scalar shell
  python mylogic.py --vector           # Force vector shell
  python mylogic.py --file design.v    # Load file and auto-detect mode
  python mylogic.py --debug            # Start with debug logging
        """
    )
    
    parser.add_argument("--version", "-v", action="version", version=f"{DESCRIPTION} v{VERSION}")
    parser.add_argument("--debug", "-d", action="store_true", 
                       help="Enable debug logging")
    parser.add_argument("--config", "-c", type=str, 
                       help="Configuration file path")
    parser.add_argument("--file", "-f", type=str,
                       help="Verilog file to load")
    parser.add_argument("--scalar", action="store_true",
                       help="Force scalar shell")
    parser.add_argument("--vector", action="store_true",
                       help="Force vector shell")
    parser.add_argument("--check-deps", action="store_true",
                       help="Check dependencies and exit")
    parser.add_argument("--synthesize", "-s", type=str, choices=["basic", "standard", "aggressive"],
                       help="Run complete synthesis flow and exit (requires --file)")
    
    args = parser.parse_args()
    
    # Handle special commands
    if args.check_deps:
        check_dependencies()
        return
    
    # Handle synthesis mode
    if args.synthesize:
        if not args.file:
            print("[ERROR] --synthesize requires --file option")
            sys.exit(1)
        run_synthesis_mode(args.file, args.synthesize, args.debug)
        return
    
    # Setup logging
    log_file = "logs/mylogic.log"
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    setup_logging(args.debug, log_file)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config = load_config(args.config or "config/mylogic_config.json")
        
        # Determine shell mode
        mode = "auto"
        if args.scalar:
            mode = "scalar"
        elif args.vector:
            mode = "vector"
        elif args.file:
            # Auto-detect based on file
            file_type = detect_file_type(args.file)
            if file_type == "vector":
                mode = "vector"
            elif file_type == "scalar":
                mode = "scalar"
            else:
                mode = "vector"  # Default to vector
        
        # If no file and no explicit mode, default to vector
        if mode == "auto":
            mode = "vector"
        
        # Check dependencies
        check_dependencies()
        
        # Create and run shell
        logger.info(f"Starting {DESCRIPTION} v{VERSION} in {mode} mode")
        shell = create_shell(mode, config, args.file)
        show_usage_info(mode)
        
        shell.run()
        
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
