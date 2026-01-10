# ModelSim compile and run script for test_memory
vlib work
vmap work work

# Compile files
vlog -work work test_memory.v test_memory_tb.v

# Run simulation
vsim -c -do "run -all; quit -f" test_memory_tb
