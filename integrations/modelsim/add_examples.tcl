#!/usr/bin/tclsh
# ModelSim TCL Script
# Add example files from Examples directory to ModelSim project (NO COMPILATION)
#
# Usage in ModelSim:
#   do add_examples_only.tcl
#   Or: source add_examples_only.tcl
#
# This script:
# 1. Opens the project (if exists) or creates new project
# 2. Adds all Verilog files from examples/ directory to the project
# 3. Does NOT compile (compile later from GUI or separate script)

# Get current script directory
set script_dir [file dirname [file normalize [info script]]]
set project_dir $script_dir
set examples_dir [file normalize [file join $project_dir .. .. examples]]
set project_file [file join $project_dir verify_with_modelsim.mpf]

puts "=========================================="
puts "Adding Example Files to ModelSim Project"
puts "=========================================="
puts "Project directory: $project_dir"
puts "Examples directory: $examples_dir"
puts "Project file: $project_file"
puts ""

# Quit simulation if running (needed before changing directory)
if {[catch {quit -sim} result]} {
    # No simulation running, that's fine
}

# Change to project directory (only if not already there)
set current_dir [pwd]
if {$current_dir != $project_dir} {
    cd $project_dir
}

# Open or create project
if {[file exists $project_file]} {
    project open $project_file
    puts "Opened existing project: verify_with_modelsim"
} else {
    project new $project_dir verify_with_modelsim
    puts "Created new project: verify_with_modelsim"
}
puts ""

# Function to recursively find all .v files
proc find_verilog_files {dir} {
    set files {}
    if {[catch {glob -nocomplain -directory $dir -types f *.v} dir_files] == 0} {
        foreach file $dir_files {
            lappend files $file
        }
    }
    
    # Recursively search subdirectories
    if {[catch {glob -nocomplain -directory $dir -types d *} subdirs] == 0} {
        foreach subdir $subdirs {
            set subdir_files [find_verilog_files $subdir]
            set files [concat $files $subdir_files]
        }
    }
    
    return $files
}

# Find all Verilog files in examples directory
puts "Searching for Verilog files in examples directory..."
set verilog_files [find_verilog_files $examples_dir]

if {[llength $verilog_files] == 0} {
    puts "WARNING: No Verilog files found in examples directory: $examples_dir"
    puts "Please check the path is correct."
    exit 1
}

puts "Found [llength $verilog_files] Verilog file(s)"
puts ""

# Add files to project (NO COMPILATION)
puts "Adding files to project (NO COMPILATION)..."
puts "----------------------------------------"

set added_count 0
set failed_count 0
set failed_files {}

foreach file $verilog_files {
    set file_name [file tail $file]
    set file_path $file
    
    # Add file to project
    if {[catch {project addfile $file_path} result]} {
        puts "  WARNING: Failed to add $file_name"
        puts "  Error: $result"
        incr failed_count
        lappend failed_files $file_name
    } else {
        puts "  Added: $file_name"
        incr added_count
    }
}

puts ""
puts "=========================================="
puts "Summary"
puts "=========================================="
puts "Total files: [llength $verilog_files]"
puts "Added to project: $added_count"
puts "Failed: $failed_count"

if {$failed_count > 0} {
    puts ""
    puts "Failed files:"
    foreach file $failed_files {
        puts "  - $file"
    }
}

puts ""
puts "=========================================="
puts "Files added to project successfully!"
puts "=========================================="
puts ""
puts "Files are now in the project but NOT compiled."
puts "To compile, use:"
puts "  - Right-click files in Project window and select 'Compile'"
puts "  - Or run: do compile_examples.tcl"
puts ""
puts "To simulate a module, first compile it, then:"
puts "  vsim <module_name>"
puts "  add wave -radix hex /*"
puts "  run 100ns"

