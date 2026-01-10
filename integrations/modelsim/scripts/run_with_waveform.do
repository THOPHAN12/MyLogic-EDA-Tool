# Simulation script with VCD waveform output
# Usage: do scripts/run_with_waveform.do <module_name>
#
# This script runs simulation and generates VCD file for waveform viewing
# VCD file can be opened with GTKWave or ModelSim viewer

# Get module name from argument or use default
if {[llength $argv] > 0} {
    set module_name [lindex $argv 0]
} else {
    set module_name "simple_and"
}

puts "========================================"
puts "ModelSim Simulation with VCD Waveform"
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

# Run simulation and generate VCD
puts "Running simulation and generating VCD waveform..."
vsim -c -do "
    add wave -radix binary /${module_name}_tb/*
    run -all
    write format vcd -output ../simulations/${module_name}/${module_name}_waveform.vcd
    quit -f
" ${module_name}_tb

puts ""
puts "Simulation completed!"
puts "VCD waveform saved to: simulations/${module_name}/${module_name}_waveform.vcd"
puts "Open with: gtkwave simulations/${module_name}/${module_name}_waveform.vcd"


