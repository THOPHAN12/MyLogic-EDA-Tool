# Batch simulation script (no GUI, auto-run and quit)
# Usage: do scripts/run_batch.do <module_name>
#
# This script compiles and runs simulation in batch mode
# Output is written to console/log file

# Get module name from argument or use default
if {[llength $argv] > 0} {
    set module_name [lindex $argv 0]
} else {
    set module_name "simple_and"
}

puts "========================================"
puts "ModelSim Batch Simulation"
puts "========================================"
puts "Module: $module_name"
puts ""

# Create work library
if {[file exists work]} {
    puts "Work library already exists"
} else {
    vlib work
    puts "Created work library"
}
vmap work work

# Compile files
puts "\nCompiling Verilog files..."
vlog -work work ${module_name}_original.v ${module_name}_mapped.v ${module_name}_tb.v

# Check for compilation errors
if {$errorCode != 0} {
    puts "ERROR: Compilation failed!"
    exit 1
}

puts "Compilation successful!"
puts ""

# Run simulation (batch mode - no GUI)
puts "Running simulation..."
vsim -c -do "
    run -all
    quit -f
" ${module_name}_tb

puts ""
puts "Simulation completed!"


