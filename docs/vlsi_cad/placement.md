# Placement (Random, Force-Directed, Simulated Annealing)

## Mục tiêu
- Đặt cells lên chip nhằm tối thiểu hóa wirelength (HPWL) và thỏa ràng buộc.

## Kiến trúc mã nguồn
- File: `core/vlsi_cad/placement.py`
- Thực thể chính:
  - `Cell`, `Net`
  - `PlacementEngine(chip_width, chip_height)`

### API chính
- Quản lý đối tượng: `add_cell(cell)`, `add_net(net)`
- Thuật toán:
  - `random_placement()`
  - `force_directed_placement(iterations=100)` (spring-mass model)
  - `simulated_annealing_placement(T0, cooling_rate, max_iter)`
- Thống kê: `get_placement_statistics()`, `visualize_placement()`

### Dòng chảy thực thi
- Random: gán vị trí ngẫu nhiên trong biên.
- Force-directed: lặp tính lực hút về tâm net, cập nhật vị trí có damping.
- Simulated annealing: nhận hàng xóm (di chuyển ngẫu nhiên), chấp nhận theo Δwirelength và nhiệt độ.

## Ví dụ
```python
from core.vlsi_cad.placement import PlacementEngine, Cell, Net
engine = PlacementEngine(1000, 1000)
engine.add_cell(Cell("a", 50, 50))
engine.add_cell(Cell("b", 60, 40))
engine.add_net(Net("n1", ["a", "b"]))
engine.random_placement()
print(engine.get_placement_statistics())
```
