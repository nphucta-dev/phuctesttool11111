# Tài Liệu Phân Tích & Thiết Kế Giải Pháp
## Hệ Thống Quản Lý Nội Dung E-Learning — Rikkei Academy LMS Simulator Pro

## 1. Sơ đồ kiến trúc & phân cấp kế thừa

```
                         ┌────────────────────────┐
                         │    BaseLesson (ABC)     │
                         │  - platform_name         │
                         │  - base_completion_points│
                         │  - __duration_minutes    │
                         │  + duration_minutes (property, read-only)│
                         │  + calculate_completion_score() (abstract)│
                         │  + update_content()      (abstract)│
                         │  + __add__ / __lt__      │
                         │  + validate_lesson_code() (static)  │
                         │  + update_base_points()  (classmethod)│
                         └────────────┬─────────────┘
                    ┌─────────────────┴───────────────────┐
                    │                                      │
          ┌─────────▼──────────┐                 ┌─────────▼──────────┐
          │    VideoLesson      │                 │  CodingChallenge   │
          │  - video_quality    │                 │  - number_of_testcases│
          │  - view_count       │                 │  - difficulty_multiplier│
          │  + calculate_score()│                 │  + calculate_score()│
          │    base + dur*0.5   │                 │    base*tests*mult  │
          │  + update_content() │                 │  + update_content() │
          │    (cập nhật thời lượng)│              │    (cập nhật testcases)│
          │  + play_video()     │                 └─────────┬──────────┘
          └─────────┬───────────┘                           │
                    │       (đa kế thừa kiểu "diamond")      │
                    └──────────────────┬─────────────────────┘
                              ┌─────────▼──────────┐
                              │  HybridAssessment   │
                              │  (kế thừa CẢ 2 nhánh)│
                              │  override calculate/ │
                              │  update_content để  │
                              │  kết hợp đúng logic │
                              └─────────────────────┘
```

`BaseLesson` là bộ khung chuẩn, quy định mọi bài học bắt buộc phải đóng gói thời lượng (`__duration_minutes` private, chỉ đọc qua `property duration_minutes`), bắt buộc tự định nghĩa `calculate_completion_score()` và `update_content()` (abstract methods), được trang bị sẵn toán tử nạp chồng `__add__`/`__lt__`, 1 static method và 1 class method dùng chung.

`VideoLesson` và `CodingChallenge` là hai nhánh kế thừa đơn trực tiếp từ `BaseLesson`, mỗi lớp override các phương thức theo nghiệp vụ riêng (video tính điểm theo thời lượng, coding tính điểm theo số testcase × hệ số khó).

`HybridAssessment` kế thừa kiểu "hình thoi" (diamond) từ CẢ HAI lớp cha, tạo ra bài toán xung đột phương thức cần giải quyết thủ công.

## 2. Báo cáo kỹ thuật

### 2.1. MRO của HybridAssessment & cách giải quyết xung đột phương thức

Khai báo `class HybridAssessment(VideoLesson, CodingChallenge)` dựng MRO:

```
HybridAssessment -> VideoLesson -> CodingChallenge -> BaseLesson -> ABC -> object
```

**Xung đột calculate_completion_score():** nếu không override, Python chọn `VideoLesson.calculate_completion_score()` (đứng trước) -- chỉ tính điểm theo thời lượng, bỏ sót hoàn toàn điểm testcase. `HybridAssessment` override rõ ràng, kết hợp cả hai:

```python
def calculate_completion_score(self):
    video_score  = VideoLesson.calculate_completion_score(self)    # base + duration*0.5
    coding_score = CodingChallenge.calculate_completion_score(self) # base*testcases*multiplier
    return video_score + coding_score - self.base_completion_points # trừ 1 lần base (đếm 2 lần)
```

**Xung đột update_content():** `VideoLesson.update_content()` cập nhật thời lượng; `CodingChallenge.update_content()` cập nhật số testcase. `HybridAssessment` chọn hành vi CodingChallenge vì vai trò kiểm tra tổng hợp yêu cầu quản lý testcase là tính năng chính:

```python
def update_content(self, new_data):
    return CodingChallenge.update_content(self, new_data)
```

**Khởi tạo cooperative `__init__`:** chuỗi `super().__init__(**kwargs)` theo đúng MRO:
```
HybridAssessment -> VideoLesson (gán video_quality, view_count)
                 -> CodingChallenge (gán number_of_testcases, difficulty_multiplier)
                 -> BaseLesson (gán lesson_code, title, duration_minutes)
```

Toàn bộ thuộc tính từ cả 2 nhánh cha được khởi tạo đầy đủ chỉ với một lệnh `super().__init__()` duy nhất ở `HybridAssessment`.

### 2.2. Vì sao Duck Typing giúp tích hợp nhà cung cấp cloud mới mà không cần sửa code gốc

Hàm `sync_to_cloud(cloud_service, lesson)` không kiểm tra `isinstance(cloud_service, SomeCloudInterface)`. Điều duy nhất nó quan tâm là đối tượng truyền vào có phương thức `upload_lesson(lesson)` hay không -- triết lý Duck Typing.

Khi Rikkei Academy muốn tích hợp thêm Azure Blob Storage, Huawei Cloud, hay bất kỳ CDN nào, kỹ sư chỉ cần viết một lớp mới có `upload_lesson()` đúng chữ ký -- không đụng đến `BaseLesson`, không đụng đến `sync_to_cloud()`, không đụng đến bất kỳ lớp bài học nào đã tồn tại. Hệ thống mở rộng được vô hạn nhà cung cấp mới mà rủi ro phá vỡ code cũ gần như bằng không.

## 3. Xử lý các bẫy dữ liệu (Edge Cases)

| Bẫy | Vị trí xử lý | Cơ chế |
|---|---|---|
| 1. Khởi tạo trực tiếp `BaseLesson` | `lesson_models.py` | `ABCMeta` tự động ném `TypeError` vì `calculate_completion_score` và `update_content` là `@abstractmethod` chưa triển khai |
| 2. Thời lượng / testcase <= 0 | `feature_create_lesson.py` (kiểm tra khi nhập), `VideoLesson.update_content()`, `CodingChallenge.update_content()` | Kiểm tra `if new_data <= 0: raise ValueError(...)` trước khi cập nhật |
| 3. Cộng/so sánh với kiểu dữ liệu sai | `BaseLesson.__add__` / `__lt__` | `isinstance(other, BaseLesson)`, nếu sai kiểu `return NotImplemented` → Python tự ném `TypeError` chuẩn |
| 4. Cloud service thiếu `upload_lesson` | `cloud_storage.sync_to_cloud()` | `try...except AttributeError`, in thông báo "Dịch vụ lưu trữ đám mây không hợp lệ hoặc chưa ký kết chứng chỉ API liên thông" |

## 4. Cấu trúc module của dự án

- `lesson_models.py` — toàn bộ các lớp bài học (BaseLesson, VideoLesson, CodingChallenge, HybridAssessment).
- `cloud_storage.py` — các lớp dịch vụ đám mây (AWSS3StorageService, GoogleCloudStorageService) và hàm `sync_to_cloud()`.
- `utils.py` — hàm tiện ích dùng chung (parse số từ input người dùng).
- `feature_create_lesson.py` — Chức năng 1.
- `feature_view_lesson.py` — Chức năng 2.
- `feature_update_content.py` — Chức năng 3.
- `feature_completion_score.py` — Chức năng 4.
- `feature_compare_duration.py` — Chức năng 5.
- `feature_cloud_sync.py` — Chức năng 6.
- `main.py` — chương trình chính, quản lý state `lessons` (list) và `current_lesson`.
