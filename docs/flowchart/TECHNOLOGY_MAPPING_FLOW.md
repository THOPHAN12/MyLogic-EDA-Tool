# Technology Mapping Flow - Detailed Flowchart

## 1. TECHNOLOGY MAPPING FLOW (OVERVIEW)

```mermaid
flowchart TD
    Start([Start Technology Mapping]) --> LoadNetlist[Load Optimized Netlist<br/>From Synthesis Flow]
    LoadNetlist --> LoadLibrary[Load Technology Library<br/>ASIC/FPGA Library]
    LoadLibrary --> SelectStrategy{Select Strategy}
    SelectStrategy -->|area| AreaOpt[Area-Optimal Mapping]
    SelectStrategy -->|delay| DelayOpt[Delay-Optimal Mapping]
    SelectStrategy -->|balanced| BalancedOpt[Balanced Mapping]
    
    AreaOpt --> ProcessNodes[Process Each Logic Node]
    DelayOpt --> ProcessNodes
    BalancedOpt --> ProcessNodes
    
    ProcessNodes --> ExtractFunction[Extract Boolean Function<br/>from Node]
    ExtractFunction --> NormalizeFunc[Normalize Function<br/>Replace variables with A,B,C...]
    NormalizeFunc --> FindCells[Find Matching Cells<br/>in Library]
    FindCells --> SelectBest{Select Best Cell<br/>Based on Strategy}
    
    SelectBest -->|area| MinArea[Minimize Area]
    SelectBest -->|delay| MinDelay[Minimize Delay]
    SelectBest -->|balanced| MinCost[Minimize Weighted Cost<br/>area + delay*10]
    
    MinArea --> MapNode[Map Node to Cell]
    MinDelay --> MapNode
    MinCost --> MapNode
    
    MapNode --> MoreNodes{More Nodes?}
    MoreNodes -->|Yes| ProcessNodes
    MoreNodes -->|No| CalculateStats[Calculate Statistics<br/>Total Area/Delay<br/>Cell Usage]
    CalculateStats --> GenerateReport[Generate Mapping Report]
    GenerateReport --> End([End Technology Mapping])
    
    style Start fill:#90EE90,stroke:#2E7D32,stroke-width:3px
    style End fill:#FFB6C1,stroke:#C2185B,stroke-width:3px
    style LoadLibrary fill:#87CEEB,stroke:#1976D2,stroke-width:2px
    style ProcessNodes fill:#FFA500,stroke:#F57C00,stroke-width:2px
    style MapNode fill:#98FB98,stroke:#2E7D32,stroke-width:2px
```

## 2. LIBRARY LOADING FLOW

```mermaid
flowchart TD
    Start([Load Library]) --> CheckPath{Library Path?}
    CheckPath -->|auto| ScanDir[Scan techlibs/ Directory<br/>Find available libraries]
    CheckPath -->|specific| DirectPath[Use Direct Path]
    
    ScanDir --> CheckType{Library Type?}
    CheckType -->|asic| ASICLib[Load ASIC Library<br/>techlibs/asic/]
    CheckType -->|fpga_common| CommonLib[Load Common FPGA<br/>techlibs/fpga/common/]
    CheckType -->|ice40| Ice40Lib[Load iCE40 Library<br/>techlibs/fpga/ice40/]
    CheckType -->|xilinx| XilinxLib[Load Xilinx Library<br/>techlibs/fpga/xilinx/]
    
    DirectPath --> DetectFormat{Detect File Format}
    ASICLib --> DetectFormat
    CommonLib --> DetectFormat
    Ice40Lib --> DetectFormat
    XilinxLib --> DetectFormat
    
    DetectFormat -->|.lib| ParseLiberty[Parse Liberty Format<br/>Extract cells, area, delay]
    DetectFormat -->|.json| ParseJSON[Parse JSON Format<br/>Load cell definitions]
    DetectFormat -->|.v| ParseVerilog[Parse Verilog Cells<br/>Extract from simcells.v]
    
    ParseLiberty --> CreateLibrary[Create TechnologyLibrary<br/>Add all cells]
    ParseJSON --> CreateLibrary
    ParseVerilog --> CreateLibrary
    
    CreateLibrary --> BuildFunctionMap[Build Function Map<br/>Normalize functions<br/>Index by function]
    BuildFunctionMap --> End([Library Ready])
    
    style Start fill:#90EE90,stroke:#2E7D32,stroke-width:3px
    style End fill:#FFB6C1,stroke:#C2185B,stroke-width:3px
    style ParseLiberty fill:#87CEEB,stroke:#1976D2,stroke-width:2px
    style ParseJSON fill:#87CEEB,stroke:#1976D2,stroke-width:2px
    style ParseVerilog fill:#87CEEB,stroke:#1976D2,stroke-width:2px
    style BuildFunctionMap fill:#FFA500,stroke:#F57C00,stroke-width:2px
```

## 3. FUNCTION NORMALIZATION FLOW

```mermaid
flowchart TD
    Start([Function Normalization]) --> InputFunc[Input Function<br/>e.g. AND a,b OR C,D XOR temp1,temp2]
    InputFunc --> ExtractName[Extract Function Name<br/>AND, OR, XOR, etc.]
    ExtractName --> ExtractArgs[Extract Arguments<br/>a,b or C,D or temp1,temp2]
    ExtractArgs --> CountArgs[Count Arguments<br/>Number of inputs]
    CountArgs --> GenerateCanonical[Generate Canonical Names<br/>A, B, C, D, ...]
    GenerateCanonical --> ReplaceArgs[Replace Arguments<br/>with Canonical Names]
    ReplaceArgs --> Reconstruct[Reconstruct Function<br/>FunctionName CanonicalArgs]
    Reconstruct --> Output[Output Normalized Function<br/>e.g. AND A,B OR A,B XOR A,B]
    Output --> End([End Normalization])
    
    style Start fill:#90EE90,stroke:#2E7D32,stroke-width:3px
    style End fill:#FFB6C1,stroke:#C2185B,stroke-width:3px
    style ExtractName fill:#87CEEB,stroke:#1976D2,stroke-width:2px
    style GenerateCanonical fill:#FFA500,stroke:#F57C00,stroke-width:2px
    style Reconstruct fill:#98FB98,stroke:#2E7D32,stroke-width:2px
```

## 4. CELL SELECTION FLOW

```mermaid
flowchart TD
    Start([Cell Selection]) --> NormalizedFunc[Normalized Function<br/>e.g. AND A,B]
    NormalizedFunc --> LookupFunction[Lookup in Function Map<br/>Find all matching cells]
    LookupFunction --> FoundCells{Found<br/>Matching Cells?}
    
    FoundCells -->|No| NoMatch[No Matching Cell<br/>Node Unmapped]
    FoundCells -->|Yes| GetStrategy{Mapping<br/>Strategy?}
    
    GetStrategy -->|area| AreaSelection[Select Cell with<br/>Minimum Area]
    GetStrategy -->|delay| DelaySelection[Select Cell with<br/>Minimum Delay]
    GetStrategy -->|balanced| BalancedSelection[Select Cell with<br/>Minimum Weighted Cost<br/>area + delay*10]
    
    AreaSelection --> CompareArea[Compare All Cells<br/>Find min area]
    DelaySelection --> CompareDelay[Compare All Cells<br/>Find min delay]
    BalancedSelection --> CompareCost[Compare All Cells<br/>Find min cost]
    
    CompareArea --> SelectBest[Select Best Cell]
    CompareDelay --> SelectBest
    CompareCost --> SelectBest
    
    SelectBest --> MapCell[Map Node to Cell<br/>Set mapped_cell<br/>Set mapping_cost]
    MapCell --> End([Cell Selected])
    NoMatch --> End
    
    style Start fill:#90EE90,stroke:#2E7D32,stroke-width:3px
    style End fill:#FFB6C1,stroke:#C2185B,stroke-width:3px
    style LookupFunction fill:#87CEEB,stroke:#1976D2,stroke-width:2px
    style SelectBest fill:#FFA500,stroke:#F57C00,stroke-width:2px
    style MapCell fill:#98FB98,stroke:#2E7D32,stroke-width:2px
```

## 5. MAPPING STRATEGIES COMPARISON

```mermaid
flowchart TD
    Start([Mapping Strategy Selection]) --> Strategy{Strategy?}
    
    Strategy -->|area| AreaFlow[Area-Optimal Flow]
    Strategy -->|delay| DelayFlow[Delay-Optimal Flow]
    Strategy -->|balanced| BalancedFlow[Balanced Flow]
    
    AreaFlow --> AreaLoop[For Each Node:<br/>Find cells matching function<br/>Select cell with min area<br/>Map node to cell]
    DelayFlow --> DelayLoop[For Each Node:<br/>Find cells matching function<br/>Select cell with min delay<br/>Map node to cell]
    BalancedFlow --> BalancedLoop[For Each Node:<br/>Find cells matching function<br/>Select cell with min cost<br/>cost = area + delay*10<br/>Map node to cell]
    
    AreaLoop --> AreaStats[Calculate:<br/>Total Area<br/>Cell Usage]
    DelayLoop --> DelayStats[Calculate:<br/>Total Delay<br/>Cell Usage]
    BalancedLoop --> BalancedStats[Calculate:<br/>Total Area<br/>Total Delay<br/>Cell Usage]
    
    AreaStats --> End([Mapping Complete])
    DelayStats --> End
    BalancedStats --> End
    
    style Start fill:#90EE90,stroke:#2E7D32,stroke-width:3px
    style End fill:#FFB6C1,stroke:#C2185B,stroke-width:3px
    style AreaFlow fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px
    style DelayFlow fill:#E3F2FD,stroke:#1976D2,stroke-width:2px
    style BalancedFlow fill:#FFF3E0,stroke:#F57C00,stroke-width:2px
```

## 6. COMPLETE TECHNOLOGY MAPPING PIPELINE

```mermaid
flowchart TD
    Start([Technology Mapping Pipeline]) --> Input[Input: Optimized Netlist<br/>After Synthesis Flow]
    Input --> InitMapper[Initialize TechnologyMapper<br/>Create mapper instance]
    InitMapper --> LoadLib[Load Technology Library<br/>From techlibs/]
    LoadLib --> ParseLib[Parse Library File<br/>Liberty/JSON/Verilog]
    ParseLib --> BuildMap[Build Function Map<br/>Index cells by function]
    BuildMap --> AddNodes[Add Logic Nodes<br/>From Netlist]
    AddNodes --> SelectStrat[Select Mapping Strategy<br/>area/delay/balanced]
    SelectStrat --> ProcessAll[Process All Nodes]
    
    ProcessAll --> ForEach[For Each Node]
    ForEach --> GetFunc[Get Node Function]
    GetFunc --> Normalize[Normalize Function]
    Normalize --> Match[Match with Library]
    Match --> Select[Select Best Cell]
    Select --> Map[Map Node to Cell]
    Map --> Next{More Nodes?}
    Next -->|Yes| ForEach
    Next -->|No| CalcStats[Calculate Statistics]
    
    CalcStats --> TotalArea[Total Area]
    CalcStats --> TotalDelay[Total Delay]
    CalcStats --> CellUsage[Cell Usage Count]
    CalcStats --> SuccessRate[Mapping Success Rate]
    
    TotalArea --> GenReport[Generate Report]
    TotalDelay --> GenReport
    CellUsage --> GenReport
    SuccessRate --> GenReport
    
    GenReport --> Output[Output: Mapped Netlist<br/>With Cell Assignments]
    Output --> End([End Pipeline])
    
    style Start fill:#90EE90,stroke:#2E7D32,stroke-width:3px
    style End fill:#FFB6C1,stroke:#C2185B,stroke-width:3px
    style LoadLib fill:#87CEEB,stroke:#1976D2,stroke-width:2px
    style ProcessAll fill:#FFA500,stroke:#F57C00,stroke-width:2px
    style Map fill:#98FB98,stroke:#2E7D32,stroke-width:2px
```

