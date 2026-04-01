# Cursor Workspace Guidance

Agent phai doc file nay truoc khi thuc hien cong viec dang ke trong repository nay.

## Superpowers plugin

- Neu Cursor da cai `superpowers`, uu tien workflow va skills cua plugin truoc.
- Local rules trong repo nay dong vai tro fallback de giu hanh vi on dinh khi plugin chua co hoac chua kich hoat.
- Lenh cai plugin trong Cursor Agent chat: `/add-plugin superpowers`

## Lo trinh agentic mac dinh

### Buoc 0: Context first

- Doc file nay truoc.
- Doc them cac tai lieu lien quan trong `docs/`, rule trong `.cursor/rules/`, va ghi chu task neu can.
- Neu yeu cau chua ro, phai lam ro muc tieu hoac thu thap ngu canh toi thieu truoc khi sua.

### Buoc 1: OpenSpec

- Can thong nhat muc tieu, pham vi, gia dinh, va cach tiep can truoc khi code.
- Voi task khong don gian, can co tom tat ke hoach ngan gon truoc khi implementation.
- Uu tien doc `docs/openspec/README.md` va dung `docs/openspec/TEMPLATE.md` lam khung mac dinh.
- Neu `superpowers` da hoat dong, xem OpenSpec local nay la ban tuong thich toi gian voi workflow brainstorming/spec cua plugin.

### Buoc 2: Superpowers

- Lam theo quy trinh: inspect -> plan -> implement -> verify.
- Uu tien duong dan tuong doi theo root repo.
- Khong hard-code duong dan tuyet doi theo may khi co the tranh duoc.
- Sau khi sua, chay demo, test, hoac command xac minh phu hop voi phan vua doi.

### Buoc 3: Beads

- Giu continuity cua task trong suot cuoc hoi thoai.
- Tai su dung cac ket luan, rang buoc, va quyet dinh da duoc xac nhan.
- Neu phat sinh convention moi huu ich, dua vao rule hoac tai lieu de lan sau agent doc duoc ngay.

## Quy tac rieng cho MyLogic

- Xac dinh root repo truoc khi chay command.
- Khi chay flow demo/testbench, uu tien thuc thi tu root cua repo hien tai.
- Canh giac voi cac script cu con tro toi path cu; uu tien suy ra path tu vi tri file script hoac root repo.
- Khi task khong nho, chot OpenSpec truoc roi moi sua code hoac chay flow.
