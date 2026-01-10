# Complete Flow Flowchart

Flow chart cho Complete Flow: Synthesis → Optimization → Technology Mapping

## Mermaid Flowchart

```mermaid
flowchart TD
    Start([Start]) --> Input[Input: Netlist]
    
    %% Synthesis
    Input --> Synth[STEP 1: SYNTHESIS<br/>Netlist → AIG]
    Synth --> SynthCheck{AIG Valid?}
    SynthCheck -->|Yes| SynthOK[AIG Created]
    SynthCheck -->|No| Error1[Error: Stop]
    
    %% Optimization Decision
    SynthOK --> OptCheck{Optimization<br/>enabled?}
    OptCheck -->|Yes| OptRun[STEP 2: OPTIMIZATION<br/>AIG → Optimized AIG<br/>- Strash<br/>- DCE<br/>- CSE<br/>- ConstProp<br/>- Balance]
    OptCheck -->|No| SkipOpt[Skip Optimization<br/>Use Original AIG]
    
    OptRun --> OptOK[Optimized AIG]
    SkipOpt --> TechCheck
    OptOK --> TechCheck{Technology<br/>Mapping<br/>enabled?}
    
    %% Technology Mapping
    TechCheck -->|Yes| TechLoad[Load Technology Library]
    TechCheck -->|No| SkipTech[Skip Techmap]
    
    TechLoad --> TechMap[STEP 3: TECHNOLOGY MAPPING<br/>AIG → Mapped Netlist<br/>Strategy: area/delay/balanced]
    TechMap --> TechOK[Technology-mapped Netlist]
    
    SkipTech --> Summary
    TechOK --> Summary[Generate Summary Report]
    
    Summary --> End([End: Return Results])
    Error1 --> End
    
    style Start fill:#90EE90
    style End fill:#90EE90
    style Synth fill:#87CEEB
    style OptRun fill:#87CEEB
    style TechMap fill:#87CEEB
    style SynthOK fill:#98FB98
    style OptOK fill:#98FB98
    style TechOK fill:#98FB98
    style Error1 fill:#FFB6C1
```

## ASCII Art Flowchart

```
                    ┌─────────────┐
                    │   START     │
                    │  run_       │
                    │ complete_   │
                    │ flow()      │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Input:    │
                    │  Netlist    │
                    │  Dictionary │
                    └──────┬──────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────┐
    │  STEP 1: SYNTHESIS                           │
    │  Netlist → AIG                               │
    │  ──────────────────────                      │
    │  • Validate netlist                          │
    │  • Convert to AIG                            │
    │  • Create AIG nodes                          │
    └──────────────────┬───────────────────────────┘
                       │
                       ▼
                ┌──────────────┐
                │ AIG Created  │
                └──────┬───────┘
                       │
                       ▼
    ┌──────────────────────────────────────────────┐
    │  STEP 2: OPTIMIZATION?                       │
    │  (enable_optimization)                       │
    └──────┬──────────────────┬────────────────────┘
           │                  │
        Yes│                  │No
           │                  │
           ▼                  ▼
    ┌─────────────┐   ┌──────────────┐
    │ Optimize    │   │ Skip Opt     │
    │ AIG         │   │ Use Original │
    │ ──────────  │   │ AIG          │
    │ • Strash    │   └──────┬───────┘
    │ • DCE       │          │
    │ • CSE       │          │
    │ • ConstProp │          │
    │ • Balance   │          │
    └──────┬──────┘          │
           │                 │
           └────────┬────────┘
                    │
                    ▼
    ┌──────────────────────────────────────────────┐
    │  STEP 3: TECHNOLOGY MAPPING?                 │
    │  (enable_techmap)                            │
    └──────┬──────────────────┬────────────────────┘
           │                  │
        Yes│                  │No
           │                  │
           ▼                  ▼
    ┌─────────────┐   ┌──────────────┐
    │ Load        │   │ Skip Techmap │
    │ Library     │   └──────┬───────┘
    └──────┬──────┘          │
           │                 │
           ▼                 │
    ┌─────────────┐          │
    │ Technology  │          │
    │ Mapping     │          │
    │ ──────────  │          │
    │ • AIG →     │          │
    │   LogicNodes│          │
    │ • Map to    │          │
    │   cells     │          │
    │ • Strategy: │          │
    │   area/     │          │
    │   delay/    │          │
    │   balanced  │          │
    └──────┬──────┘          │
           │                 │
           └────────┬────────┘
                    │
                    ▼
            ┌───────────────┐
            │   SUMMARY     │
            │   REPORT      │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │  RETURN       │
            │  RESULTS      │
            │  Dictionary   │
            └───────┬───────┘
                    │
                    ▼
                ┌───────┐
                │  END  │
                └───────┘
```

## Data Flow

```
Netlist
  │
  ├─[Synthesis]──→ AIG
  │                   │
  │                   ├─[Optimization]──→ Optimized AIG
  │                   │                      │
  │                   │                      └─[Techmap]──→ Mapped Netlist
  │                   │
  │                   └───────────────────────[Techmap]──→ Mapped Netlist
  │
  └────────────────────────────────────────────→ Results Dictionary
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant CompleteFlow
    participant Synthesis
    participant Optimization
    participant Techmap

    User->>CompleteFlow: run_complete_flow(netlist, ...)
    
    CompleteFlow->>Synthesis: synthesize(netlist)
    Synthesis-->>CompleteFlow: AIG
    
    alt Optimization enabled
        CompleteFlow->>Optimization: optimize(aig, level)
        Optimization-->>CompleteFlow: Optimized AIG
    end
    
    alt Techmap enabled
        CompleteFlow->>Techmap: techmap(aig, library, strategy)
        Techmap-->>CompleteFlow: Mapped Results
    end
    
    CompleteFlow->>CompleteFlow: Generate Summary
    CompleteFlow-->>User: Results Dictionary
```

