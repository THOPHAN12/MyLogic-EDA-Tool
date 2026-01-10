"""
Tests for Complete Synthesis Flow.
"""

import pytest
from core.synthesis.synthesis_flow import SynthesisFlow, run_complete_synthesis


class TestSynthesisFlow:
    """Test suite for Complete Synthesis Flow."""
    
    def test_basic_synthesis(self, duplicate_netlist):
        """Test basic synthesis flow."""
        result = run_complete_synthesis(duplicate_netlist, 'basic')
        
        assert isinstance(result, dict)
        assert 'nodes' in result
        assert 'wires' in result
    
    def test_standard_synthesis(self, duplicate_netlist):
        """Test standard synthesis flow."""
        result = run_complete_synthesis(duplicate_netlist, 'standard')
        
        assert isinstance(result, dict)
        assert len(result['nodes']) <= len(duplicate_netlist['nodes'])
    
    def test_aggressive_synthesis(self, duplicate_netlist):
        """Test aggressive synthesis flow."""
        result = run_complete_synthesis(duplicate_netlist, 'aggressive')
        
        assert isinstance(result, dict)
        assert len(result['nodes']) <= len(duplicate_netlist['nodes'])
    
    def test_synthesis_preserves_outputs(self, duplicate_netlist):
        """Test that synthesis preserves all outputs."""
        result = run_complete_synthesis(duplicate_netlist, 'basic')
        
        assert 'outputs' in result
        assert set(result['outputs']) == set(duplicate_netlist['outputs'])
    
    def test_synthesis_flow_class(self, duplicate_netlist):
        """Test SynthesisFlow class."""
        flow = SynthesisFlow()
        result = flow.run_complete_synthesis(duplicate_netlist, 'basic')
        
        assert isinstance(result, dict)
        assert 'nodes' in result
    
    def test_synthesis_empty_netlist(self):
        """Test synthesis with empty netlist."""
        empty_netlist = {
            'name': 'empty',
            'inputs': [],
            'outputs': [],
            'nodes': {},
            'wires': {}
        }
        
        result = run_complete_synthesis(empty_netlist, 'basic')
        
        assert len(result['nodes']) == 0

