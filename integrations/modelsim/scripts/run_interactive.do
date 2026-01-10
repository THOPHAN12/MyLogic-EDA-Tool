# Interactive simulation script (with GUI for waveform viewing)
# Usage: do scripts/run_interactive.do <module_name>
#
# This script opens ModelSim GUI with waveforms for interactive debugging

# Get module name from argument or use default
if {[llength $argv] > 0} {
    set module_name [lindex $argv 0]
} else {
    set module_name "simple_and"
}

puts "========================================"
puts "ModelSim Interactive Simulation"
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

# Run simulation with GUI
puts "Starting simulation in GUI mode..."
vsim ${module_name}_tb

# Add waves to waveform viewer
puts "Adding signals to waveform viewer..."
add wave -radix binary /${module_name}_tb/a
add wave -radix binary /${module_name}_tb/b
add wave -radix binary /${module_name}_tb/out_orig
add wave -radix binary /${module_name}_tb/out_mapped

# Add all signals if there are more (e.g., cin, sum, cout)
# Uncomment and modify as needed:
# add wave -radix binary /${module_name}_tb/*

# Run simulation
puts "Running simulation..."
run -all

puts ""
puts "Simulation completed! Waveform viewer is open."
puts "Use 'run -all' to run again, or 'quit -sim' to close simulation."


