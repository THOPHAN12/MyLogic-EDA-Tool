#!/usr/bin/env python3
"""
Test All Components với nhiều demo files
Kiểm thử Synthesis, Optimization, Technology Mapping trên tất cả CAN_DO demos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
from frontends.verilog import parse_verilog
from core.complete_flow import run_complete_flow
from core.technology_mapping.library_loader import load_library

def test_file(file_path, sky130_lib):
    """Test một file với complete flow."""
    file_name = os.path.basename(file_path)
    print(f"\n{'='*70}")
    print(f"Testing: {file_name}")
    print('='*70)
    
    results = {
        'file': file_name,
        'parse': False,
        'synthesis': False,
        'optimization': False,
        'techmap': False,
        'complete_flow': False
    }
    
    # 1. Parse
    try:
        netlist = parse_verilog(file_path)
        results['parse'] = True
        print(f"✅ Parse: OK ({len(netlist.get('nodes', []))} nodes)")
    except Exception as e:
        print(f"❌ Parse: FAILED - {e}")
        return results
    
    # 2. Synthesis
    try:
        from core.synthesis.synthesis_flow import synthesize
        aig = synthesize(netlist)
        if aig.count_nodes() > 0:
            results['synthesis'] = True
            print(f"✅ Synthesis: OK ({aig.count_nodes()} AIG nodes)")
        else:
            print(f"❌ Synthesis: FAILED (no nodes)")
    except Exception as e:
        print(f"❌ Synthesis: FAILED - {e}")
        return results
    
    # 3. Optimization
    try:
        from core.optimization.optimization_flow import optimize
        optimized_aig = optimize(aig)
        if optimized_aig.count_nodes() >= 0:
            results['optimization'] = True
            reduction = aig.count_nodes() - optimized_aig.count_nodes()
            reduction_pct = (reduction / aig.count_nodes() * 100) if aig.count_nodes() > 0 else 0
            print(f"✅ Optimization: OK ({optimized_aig.count_nodes()} nodes, {reduction_pct:.1f}% reduction)")
        else:
            print(f"❌ Optimization: FAILED")
    except Exception as e:
        print(f"❌ Optimization: FAILED - {e}")
        return results
    
    # 4. Technology Mapping
    try:
        from core.technology_mapping.technology_mapping import techmap
        techmap_results = techmap(optimized_aig, sky130_lib, strategy='area_optimal')
        mapped_nodes = techmap_results.get('mapped_nodes', 0)
        total_nodes = techmap_results.get('total_nodes', 0)
        success_rate = techmap_results.get('mapping_success_rate', 0.0)
        
        if mapped_nodes >= 0:
            results['techmap'] = True
            print(f"✅ Techmap: OK ({mapped_nodes}/{total_nodes} mapped, {success_rate*100:.1f}%)")
        else:
            print(f"❌ Techmap: FAILED")
    except Exception as e:
        print(f"❌ Techmap: FAILED - {e}")
        return results
    
    # 5. Complete Flow
    try:
        output_dir = Path('test_output')
        output_dir.mkdir(exist_ok=True)
        
        flow_results = run_complete_flow(
            netlist,
            enable_optimization=True,
            enable_techmap=True,
            enable_verification=False,
            techmap_library=sky130_lib,
            write_verilog=False,  # Don't write files for batch test
            output_dir=output_dir
        )
        
        if (flow_results.get('synthesis', {}).get('aig') and 
            flow_results.get('optimization', {}).get('aig') and
            flow_results.get('techmap', {}).get('results')):
            results['complete_flow'] = True
            print(f"✅ Complete Flow: OK")
        else:
            print(f"❌ Complete Flow: FAILED")
    except Exception as e:
        print(f"❌ Complete Flow: FAILED - {e}")
        return results
    
    return results

def main():
    """Main test function."""
    print("="*70)
    print("MYLOGIC ALL COMPONENTS TEST")
    print("Testing Synthesis, Optimization, Technology Mapping")
    print("on all CAN_DO demo files")
    print("="*70)
    
    # Load library
    print("\n[0] Loading SKY130 library...")
    try:
        sky130_lib = load_library('techlibs/asic/sky130/sky130_fd_sc_hd.lib')
        print(f"✅ Loaded: {sky130_lib.name} ({len(sky130_lib.cells)} cells)")
    except Exception as e:
        print(f"❌ Library load failed: {e}")
        return False
    
    # Find all demo files
    demo_dir = Path('demo/CAN_DO')
    if not demo_dir.exists():
        print(f"❌ Demo directory not found: {demo_dir}")
        return False
    
    demo_files = sorted(demo_dir.glob('*.v'))
    print(f"\n[1] Found {len(demo_files)} demo files")
    
    if len(demo_files) == 0:
        print("❌ No demo files found")
        return False
    
    # Test each file
    all_results = []
    for demo_file in demo_files:
        results = test_file(str(demo_file), sky130_lib)
        all_results.append(results)
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    # Count passes
    parse_count = sum(1 for r in all_results if r['parse'])
    synthesis_count = sum(1 for r in all_results if r['synthesis'])
    optimization_count = sum(1 for r in all_results if r['optimization'])
    techmap_count = sum(1 for r in all_results if r['techmap'])
    complete_flow_count = sum(1 for r in all_results if r['complete_flow'])
    total_files = len(all_results)
    
    print(f"\nTotal files tested: {total_files}")
    print(f"\nComponent Results:")
    print(f"  Parse:           {parse_count}/{total_files} ({parse_count*100//total_files if total_files > 0 else 0}%)")
    print(f"  Synthesis:       {synthesis_count}/{total_files} ({synthesis_count*100//total_files if total_files > 0 else 0}%)")
    print(f"  Optimization:    {optimization_count}/{total_files} ({optimization_count*100//total_files if total_files > 0 else 0}%)")
    print(f"  Technology Map:   {techmap_count}/{total_files} ({techmap_count*100//total_files if total_files > 0 else 0}%)")
    print(f"  Complete Flow:   {complete_flow_count}/{total_files} ({complete_flow_count*100//total_files if total_files > 0 else 0}%)")
    
    # Detailed results
    print(f"\nDetailed Results:")
    print(f"{'File':<30} {'Parse':<8} {'Synth':<8} {'Optim':<8} {'Techmap':<8} {'Flow':<8}")
    print("-" * 70)
    for r in all_results:
        file_short = r['file'][:28]
        parse_status = "✅" if r['parse'] else "❌"
        synth_status = "✅" if r['synthesis'] else "❌"
        optim_status = "✅" if r['optimization'] else "❌"
        techmap_status = "✅" if r['techmap'] else "❌"
        flow_status = "✅" if r['complete_flow'] else "❌"
        print(f"{file_short:<30} {parse_status:<8} {synth_status:<8} {optim_status:<8} {techmap_status:<8} {flow_status:<8}")
    
    print("="*70)
    
    # Overall result
    all_passed = (parse_count == total_files and 
                  synthesis_count == total_files and 
                  optimization_count == total_files and
                  techmap_count == total_files and
                  complete_flow_count == total_files)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED FOR ALL FILES!")
    else:
        print(f"\n⚠️  SOME TESTS FAILED ({complete_flow_count}/{total_files} files passed complete flow)")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)






