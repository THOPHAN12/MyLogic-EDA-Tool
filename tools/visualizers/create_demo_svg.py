#!/usr/bin/env python3
"""
Tạo file SVG demo đơn giản để xem
"""

def create_demo_svg():
    """Tạo file SVG demo."""
    
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <defs>
    <style>
      .input-box { fill: #4caf50; stroke: #2e7d32; stroke-width: 2; }
      .output-box { fill: #f44336; stroke: #c62828; stroke-width: 2; }
      .gate-box { fill: #ff9800; stroke: #f57c00; stroke-width: 2; }
      .connection-line { stroke: #333; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }
      .text { font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; }
      .label { font-family: Arial, sans-serif; font-size: 12px; }
    </style>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333" />
    </marker>
  </defs>
  
  <!-- Background -->
  <rect width="600" height="400" fill="#f5f5f5"/>
  
  <!-- Title -->
  <text x="300" y="30" text-anchor="middle" class="text" fill="#1976d2">
    MyLogic EDA Tool - Circuit Demo
  </text>
  
  <!-- Input Port -->
  <rect x="50" y="150" width="80" height="40" class="input-box" rx="5"/>
  <text x="90" y="175" text-anchor="middle" class="text" fill="white">INPUT</text>
  
  <!-- Logic Gates -->
  <rect x="200" y="120" width="80" height="40" class="gate-box" rx="5"/>
  <text x="240" y="145" text-anchor="middle" class="text" fill="white">AND</text>
  
  <rect x="200" y="200" width="80" height="40" class="gate-box" rx="5"/>
  <text x="240" y="225" text-anchor="middle" class="text" fill="white">OR</text>
  
  <!-- Output Ports -->
  <rect x="450" y="120" width="80" height="40" class="output-box" rx="5"/>
  <text x="490" y="145" text-anchor="middle" class="text" fill="white">OUT1</text>
  
  <rect x="450" y="200" width="80" height="40" class="output-box" rx="5"/>
  <text x="490" y="225" text-anchor="middle" class="text" fill="white">OUT2</text>
  
  <!-- Connections -->
  <line x1="130" y1="170" x2="200" y2="140" class="connection-line"/>
  <line x1="130" y1="170" x2="200" y2="220" class="connection-line"/>
  <line x1="280" y1="140" x2="450" y2="140" class="connection-line"/>
  <line x1="280" y1="220" x2="450" y2="220" class="connection-line"/>
  
  <!-- Connection Labels -->
  <text x="165" y="155" class="label" fill="#666">A</text>
  <text x="165" y="195" class="label" fill="#666">B</text>
  <text x="365" y="135" class="label" fill="#666">C</text>
  <text x="365" y="215" class="label" fill="#666">D</text>
  
  <!-- Features List -->
  <text x="50" y="320" class="label" fill="#1976d2">Features:</text>
  <text x="50" y="340" class="label" fill="#666">• Input ports (Green)</text>
  <text x="50" y="355" class="label" fill="#666">• Logic gates (Orange)</text>
  <text x="50" y="370" class="label" fill="#666">• Output ports (Red)</text>
  <text x="50" y="385" class="label" fill="#666">• Connection lines with arrows</text>
  
  <!-- MyLogic Logo -->
  <text x="500" y="350" class="label" fill="#1976d2">MyLogic EDA Tool</text>
  <text x="500" y="365" class="label" fill="#666">v2.0.0</text>
</svg>'''
    
    with open("examples/demo_circuit.svg", 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print("[SUCCESS] Created demo SVG: examples/demo_circuit.svg")
    print("Features:")
    print("  - Input port (Green)")
    print("  - Logic gates (Orange)")  
    print("  - Output ports (Red)")
    print("  - Connection lines with arrows")
    print("  - Professional styling")

if __name__ == "__main__":
    create_demo_svg()
