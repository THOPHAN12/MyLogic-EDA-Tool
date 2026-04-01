# OpenSpec for MyLogic

`OpenSpec` la buoc chot yeu cau truoc khi agent sua code, chay demo, hoac thay doi flow trong repository nay.

## Khi nao phai dung OpenSpec

Bat buoc dung voi cac task:

- sua logic hoac flow co anh huong den nhieu file
- thay doi command, script, hoac duong dan
- them tinh nang moi
- sua bug nhung chua ro nguyen nhan
- refactor hoac thay doi hanh vi dau ra

Co the bo qua spec day du voi task rat nho, nhung van phai neu ro:

- muc tieu
- pham vi
- cach xac minh

## Noi dung toi thieu cua OpenSpec

Truoc khi implement, agent nen chot cac muc sau:

1. Goal
2. Scope
3. Assumptions
4. Constraints
5. Plan
6. Verification

## Quy uoc trong repo nay

- Neu task khong don gian, tao spec ngan gon dua tren `docs/openspec/TEMPLATE.md`.
- Neu task chi can mot spec tam thoi trong chat, van phai bao gom 6 muc tren.
- Neu task lon hoac lap lai, luu spec thanh file trong `docs/openspec/specs/`.

## Muc tieu cua OpenSpec

- tranh sua sai bai toan
- giam hard-code va quyet dinh vo tinh
- giu cho command, flow, va test khop voi root repo hien tai
- tang kha nang tiep noi cho cac lan lam viec sau
