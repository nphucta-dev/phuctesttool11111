# -*- coding: utf-8 -*-
"""
feature_view_lesson.py
------------------------
Chức năng 2: Xem thông tin chi tiết bài học hiện tại & in danh sách MRO.
"""


def feature2_view_lesson(current_lesson):
    if current_lesson is None:
        print("\nHệ thống chưa có bài học nào. Vui lòng khởi tạo bài học ở Chức năng 1 trước.")
        return

    print("\n--- THÔNG TIN BÀI HỌC HIỆN TẠI ---")
    print(f"Loại bài học: {type(current_lesson).__name__}")
    print(f"Nền tảng: {current_lesson.platform_name}")
    print(f"Mã bài học: {current_lesson.lesson_code}")
    print(f"Tiêu đề bài học: {current_lesson.title}")
    print(f"Thời lượng bài học: {current_lesson.duration_minutes} phút")

    # Hiển thị thuộc tính riêng tùy loại bài học (đa hình về thuộc tính)
    if hasattr(current_lesson, "video_quality"):
        print(f"Chất lượng video: {current_lesson.video_quality}")
    if hasattr(current_lesson, "view_count"):
        print(f"Lượt xem: {current_lesson.view_count} lượt")
    if hasattr(current_lesson, "number_of_testcases"):
        print(f"Số lượng testcase lập trình: {current_lesson.number_of_testcases} bài")
    if hasattr(current_lesson, "difficulty_multiplier"):
        print(f"Hệ số độ khó: {current_lesson.difficulty_multiplier}")

    print("\n--- KIỂM TRA MRO (Method Resolution Order) ---")
    mro_chain = " -> ".join(cls.__name__ for cls in type(current_lesson).__mro__)
    print(mro_chain)
