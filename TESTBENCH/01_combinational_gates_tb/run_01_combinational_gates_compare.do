transcript on

set tb_file "TESTBENCH/01_combinational_gates_tb/tb_01_combinational_gates_compare.v"
set src_ref "demo/CAN_DO/01_combinational_gates.v"
set src_synth "outputs/01_combinational_gates_synthesized.v"
set src_opt "outputs/01_combinational_gates_synthesized_opt.v"

proc run_one {label src_file} {
    if {[file exists work]} {
        vdel -lib work -all
    }
    vlib work

    echo "============================================================"
    echo "RUNNING: $label"
    echo "SOURCE : $src_file"
    echo "============================================================"

    set compile_tb [eval vlog +define+DUT_LABEL=\"$label\" \"$::tb_file\"]
    if {$compile_tb != 0} {
        echo "RESULT $label FAIL: testbench compile failed."
        return 1
    }

    set compile_dut [eval vlog \"$src_file\"]
    if {$compile_dut != 0} {
        echo "RESULT $label FAIL: DUT compile failed."
        return 1
    }

    set sim_status [catch {vsim -c work.tb_01_combinational_gates_compare -do "run -all; quit -f"} sim_result]
    if {$sim_status != 0} {
        echo "RESULT $label FAIL: simulation failed."
        return 1
    }

    return 0
}

set fail_count 0

if {[run_one "original" $src_ref] != 0} {
    incr fail_count
}

if {[run_one "synthesized" $src_synth] != 0} {
    incr fail_count
}

if {[run_one "optimized" $src_opt] != 0} {
    incr fail_count
}

echo "============================================================"
if {$fail_count == 0} {
    echo "FINAL RESULT: all 3 files PASS and produce the same expected outputs."
} else {
    echo "FINAL RESULT: $fail_count run(s) FAILED."
}
echo "============================================================"

quit -f
