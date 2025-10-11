# Routing (Maze/Lee, Rip-up & Reroute)

## Mục tiêu
- Kết nối các pins trên lưới nhiều lớp với xung đột tối thiểu và wirelength hợp lý.

## Kiến trúc mã nguồn
- File: `core/vlsi_cad/routing.py`
- Thực thể chính: `Point`, `RoutingGrid(width, height, layers)`, `Net`, `MazeRouter`

### API chính
- Grid: `is_free/occupy/block/get_neighbors`
- Router: `add_net(net)`, `route_all_nets(strategy="maze|lee|rip_up_reroute")`, `get_routing_statistics()`, `visualize_routing()`

### Chiến lược
- Maze (tham lam đơn giản), Lee (wave propagation giản lược)
- Rip-up & Reroute: xóa đường đi tắc nghẽn và thử lại

### Dòng chảy thực thi (maze)
1) Sắp xếp nets theo priority và ước lượng wirelength
2) Route từng net: point-to-point; chọn hướng ưu tiên về đích, tránh ô bận
3) Nếu tắc: thử phương án thay thế; thất bại → false

## Ví dụ
```python
from core.vlsi_cad.routing import RoutingGrid, MazeRouter, Net, Point
grid = RoutingGrid(50, 50, 3)
router = MazeRouter(grid)
router.add_net(Net("n1", [Point(5,5)], [Point(45,45)]))
print(router.route_all_nets("maze"))
print(router.get_routing_statistics())
```
