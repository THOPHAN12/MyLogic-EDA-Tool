# Static Timing Analysis (STA)

## Mục tiêu
- Tính AT (arrival time), RAT (required arrival time), Slack; phát hiện critical paths.

## Kiến trúc mã nguồn
- File: `core/vlsi_cad/timing_analysis.py`
- Thực thể chính: `TimingNode`, `TimingArc`, `StaticTimingAnalyzer`

### API chính
- `add_node(node)`, `add_arc(arc)`, `set_clock_period(period)`
- `perform_timing_analysis() -> Dict[str, Any]`
- `print_timing_report(report)`

### Dòng chảy thực thi
1) AT: lan truyền tiến từ inputs
2) RAT: lan truyền lùi từ outputs (theo clock period)
3) Slack = RAT − AT; tìm đường critical; tổng hợp báo cáo

## Ví dụ
```python
from core.vlsi_cad.timing_analysis import StaticTimingAnalyzer, TimingNode, TimingArc
sta = StaticTimingAnalyzer()
sta.add_node(TimingNode("in1", "input"))
sta.add_node(TimingNode("g1", "gate"))
sta.add_node(TimingNode("out", "output"))
sta.add_arc(TimingArc("in1","g1",0.2))
sta.add_arc(TimingArc("g1","out",0.3))
sta.set_clock_period(2.0)
report = sta.perform_timing_analysis()
sta.print_timing_report(report)
```

## Ghi chú
- Mô hình trễ đơn giản; chưa gồm slew/cap/corners; có thể mở rộng khi cần.
