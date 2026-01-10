# Clean work library and temp files
# Usage: do scripts/clean.do
#
# This script removes work library and temporary files
# Useful when starting fresh or encountering library corruption

puts "========================================"
puts "Cleaning ModelSim Work Directory"
puts "========================================"
puts ""

# Quit any active simulation
catch {quit -sim}

# Remove work library mapping
catch {
    vmap -del work
    puts "Removed work library mapping"
}

# Delete work library
if {[file exists work]} {
    file delete -force work
    puts "Deleted work library directory"
} else {
    puts "Work library does not exist"
}

# Recreate work library
vlib work
vmap work work
puts "Created fresh work library"

puts ""
puts "Cleanup completed! Work library has been reset."


