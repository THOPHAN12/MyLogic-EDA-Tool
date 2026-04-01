# Superpowers Integration

Tai lieu nay dung de tich hop repo nay voi plugin `superpowers` trong Cursor.

## Muc tieu

- Uu tien workflow agentic chuan cua `superpowers`
- Giu local rules trong repo lam fallback
- Tránh xung dot giua plugin workflow va guidance noi bo

## Cach cai trong Cursor

Mo Cursor Agent chat va chay:

```text
/add-plugin superpowers
```

Tham khao: [obra/superpowers](https://github.com/obra/superpowers)

## Cach xac minh

Sau khi cai, bat dau mot chat moi va giao mot task can planning, vi du:

- "Help me plan this feature"
- "Let's debug this issue"

Plugin du kien se kich hoat skill phu hop de dua task vao workflow agentic.

## Cach repo nay phoi hop voi Superpowers

- `cursor.md` la diem vao cua workspace.
- `.cursor/rules/*.mdc` van ton tai de fallback khi plugin chua co.
- `docs/openspec/README.md` va `docs/openspec/TEMPLATE.md` la lop tuong thich toi gian cho buoc spec.

## Anh xa khai niem

- OpenSpec local <-> brainstorming/spec refinement
- Agentic flow local <-> using-superpowers + writing-plans + execution workflow
- Verification local <-> verification discipline cua plugin

## Ghi chu quan trong

- Hien tai plugin `superpowers` chua duoc phat hien trong Cursor config tren may nay.
- Vi vay repo da duoc chuan bi san de khi ban cai plugin, local guidance se khong can sua lon nua.
