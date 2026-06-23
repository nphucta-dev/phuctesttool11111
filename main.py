# -*- coding: utf-8 -*-
"""
main.py
--------
Điểm khởi chạy chương trình Rikkei E-Learning Simulator Pro.
Chỉ chịu trách nhiệm hiển thị menu và điều phối (route) sang các module
feature_*.py. Toàn bộ logic nghiệp vụ nằm trong các module riêng để dễ
quản lý, mở rộng và sửa lỗi độc lập.
"""

from feature_create_lesson import feature1_create_lesson
from feature_view_lesson import feature2_view_lesson
from feature_update_content import feature3_update_content
from feature_completion_score import feature4_completion_score
from feature_compare_duration import feature5_compare_duration
from feature_cloud_sync import feature6_cloud_sync


def main():
    # State chung của toàn hệ thống
    lessons = []           # Danh sách toàn bộ bài học đã khởi tạo
    current_lesson = None  # Bài học đang được chọn để thao tác

    while True:
        print("\n" + " RIKKEI ACADEMY LMS SIMULATOR PRO ".center(70, "="))
        print('''
        1. Khởi tạo bài học mới (Chọn loại bài học nội dung)
        2. Xem thông tin bài học & Kiểm tra thứ tự kế thừa (MRO)
        3. Cập nhật thời lượng & Nội dung bài học (Tính đa hình)
        4. Xem chi tiết điểm thưởng hoàn thành bài học
        5. Kiểm tra gộp thời lượng & So sánh độ dài bài học (Overloading)
        6. Đồng bộ bài giảng lên Nền tảng Đám mây (Duck Typing)
        7. Thoát chương trình
        ''')
        print("=" * 70)

        choice = input("Chọn chức năng (1-7): ").strip()

        match choice:
            case "1":
                new_lesson = feature1_create_lesson(lessons)
                if new_lesson is not None:
                    current_lesson = new_lesson

            case "2":
                feature2_view_lesson(current_lesson)

            case "3":
                feature3_update_content(current_lesson)

            case "4":
                feature4_completion_score(current_lesson)

            case "5":
                feature5_compare_duration(lessons, current_lesson)

            case "6":
                feature6_cloud_sync(current_lesson)

            case "7":
                print("\nCảm ơn bạn đã trải nghiệm hệ thống Quản lý Bài học Rikkei Academy LMS Pro!")
                break

            case _:
                print("\nChức năng không tồn tại!")


if __name__ == "__main__":
    main()
