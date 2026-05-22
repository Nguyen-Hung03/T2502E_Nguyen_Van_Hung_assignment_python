# HE THONG TONG HOP TIN TUC CLI (PYTHON + MYSQL)

Du an nay duoc xay dung theo de bai: quan ly nguon tin, thu thap link va thu thap noi dung chi tiet theo 2 giai doan, xem tin co phan trang, va dieu khien bo lap lich trong giao dien dong lenh.

## 1. Cau truc du an

- `sql/init_db.sql`: Tao co so du lieu `news_management`, tao 3 bang va nap san 5 chuyen muc.
- `src/main.py`: Chuong trinh menu CLI.
- `src/services/source_service.py`: Them/sua/xoa/xem bang nguon tin.
- `src/services/article_service.py`: Luu, lay va phan trang bai viet.
- `src/crawler.py`: Thu thap link va noi dung chi tiet bang `requests` + `BeautifulSoup`.
- `src/services/scheduler_service.py`: 2 tac vu lap lich voi thu vien `schedule`.
- `.env.example`: Bien moi truong mau.

## 2. Yeu cau he thong

- Python 3.10+
- MySQL 8+

## 3. Cai dat

### Buoc 1: Tao va cau hinh bien moi truong

Tao file `.env` tu `.env.example` va cap nhat thong tin phu hop:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`
- `LINK_JOB_TIME` (vi du `08:00`)
- `DETAIL_JOB_INTERVAL_MINUTES` (vi du `30`)

### Buoc 2: Cai thu vien

```bash
pip install -r requirements.txt
```

### Buoc 3: Khoi tao co so du lieu va nap du lieu mau

Dang nhap MySQL va chay:

```sql
SOURCE sql/init_db.sql;
```

Danh sach chuyen muc duoc nap san:

1. Cong nghe
2. Kinh doanh
3. The thao
4. Giai tri
5. The gioi

### Buoc 4: Chay ung dung CLI

```bash
python src/main.py
```

## 4. Mo ta chuc nang

### 4.1. Quan ly nguon tin

Menu `1. Quan ly nguon tin` cho phep:

- Them nguon tin
- Sua nguon tin
- Xoa nguon tin
- Xem danh sach nguon tin

Khi them/sua nguon tin, nguoi dung bat buoc chon `category_id` tu bang chuyen muc.

`parser_type` ho tro:

- `vnexpress`
- `tuoitre`
- `generic`

### 4.2. Xem tin tuc co phan trang

Menu `2. Xem tin tuc` su dung truy van MySQL `LIMIT/OFFSET`.

- Moi trang 10 tin
- `N`: Trang tiep
- `P`: Trang truoc
- `Q`: Thoat

### 4.3. Dieu khien bo lap lich

Menu `3. Dieu khien Cronjob`:

- Bat bo lap lich
- Tat bo lap lich
- Chay thu cong tac vu lay danh sach link
- Chay thu cong tac vu lay noi dung chi tiet

## 5. Logic thu thap 2 giai doan

### Tac vu 1 - Lay danh sach link

- Doc cac nguon tin dang hoat dong
- Trich xuat `title` + `url`
- Luu vao `articles` voi `status = 0`
- Loai bo trung qua `UNIQUE(url)` va kiem tra ton tai truoc khi them

### Tac vu 2 - Lay noi dung chi tiet

- Lay cac bai co `status = 0`
- Truy cap link bai viet
- Lay `summary`, `content`
- Cap nhat `status = 1`

## 6. Luu y ky thuat

- Da them header `User-Agent` khi gui request.
- Da xu ly ngoai le khi request loi, website chan truy cap, hoac link hong.
- Thu thap theo bo tach rieng cho VnExpress, Tuoi Tre, va du phong `generic`.

## 7. Huong dan demo

1. Chay SQL de tao co so du lieu va nap du lieu mau.
2. Them it nhat 2 nguon tin (1 VnExpress, 1 Tuoi Tre) trong menu quan ly nguon tin.
3. Chay thu cong tac vu lay danh sach link trong menu dieu khien bo lap lich.
4. Vao menu xem tin tuc de xem tin da duoc lay (status = 0).
5. Chay thu cong tac vu lay noi dung chi tiet.
6. Vao menu xem tin tuc de xem cac tin da cap nhat `status = 1`.
7. Demo phan trang voi N/P.

## 8. Video demo va Drive

- Link video demo (upload Drive): `DAN_LINK_VIDEO_DRIVE_VAO_DAY`

