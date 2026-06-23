# -*- coding: utf-8 -*-
"""
feature_update_content.py
---------------------------
Chức năng 3: Cập nhật thời lượng & Nội dung bài học (Tính đa hình).

Cùng một lệnh gọi current_lesson.update_content(new_data), nhưng hành vi
xử lý tự động thay đổi tùy loại bài học đang active:
- VideoLesson:        cập nhật thời lượng (phút).
- CodingChallenge:    cập nhật số lượng testcase.
- HybridAssessment:   gọi đích danh CodingChallenge.update_content
                      (cập nhật số testcase -- giải quyết xung đột MRO).
Đây chính là Đa hình (Polymorphism).
"""

from lesson_models import VideoLesson, CodingChallenge, HybridAssessment
from utils import parse_number


def feature3_update_content(current_lesson):
    if current_lesson is None:
        print("\nHệ thống chưa có bài học nào được chọn. Vui lòng khởi tạo/chọn bài học trước.")
        return

    print("\n--- CẬP NHẬT NỘI DUNG & THỜI LƯỢNG ---")
    print("1. Giả lập học viên tăng lượt xem video (Chỉ dành cho Video/Hybrid)")
    print("2. Cập nhật thông số bài học (Thời lượng, testcase...)")
    choice = input("Chọn tác vụ (1-2): ").strip()

    if choice == "1":
        _handle_play_video(current_lesson)
    elif choice == "2":
        _handle_update(current_lesson)
    else:
        print("Lựa chọn không hợp lệ!")


def _handle_play_video(current_lesson):
    # play_video() chỉ áp dụng cho VideoLesson và HybridAssessment
    if not isinstance(current_lesson, VideoLesson):
        print("\nBài tập Coding Challenge không hỗ trợ tác vụ phát video.")
        return
    current_lesson.play_video()
    print("\nGhi nhận thành công! Học viên đã xem video bài học.")
    print(f"Tổng số lượt xem hiện tại: {current_lesson.view_count} lượt.")


def _handle_update(current_lesson):
    # Quyết định nhập liệu tùy loại bài học
    if isinstance(current_lesson, CodingChallenge):
        # CodingChallenge (bao gồm HybridAssessment): cập nhật số testcase
        text = input("Nhập số lượng testcase kiểm thử mới bổ sung: ").strip()
        try:
            new_val = int(parse_number(text))
            current_lesson.update_content(new_val)
            print("\nCập nhật thông số thành công!")
            print(f"Số lượng testcase hiện tại trên hệ thống: {current_lesson.number_of_testcases} testcases.")
        except ValueError as e:
            print(f"Cập nhật thất bại: {e}")

    elif isinstance(current_lesson, VideoLesson):
        # VideoLesson thuần: cập nhật thời lượng
        text = input("Nhập thời lượng mới của bài học (phút): ").strip()
        try:
            new_val = int(parse_number(text))
            current_lesson.update_content(new_val)
            print("\nCập nhật thời lượng thành công!")
            print(f"Thời lượng mới: {current_lesson.duration_minutes} phút.")
        except ValueError as e:
            print(f"Cập nhật thất bại: {e}")
    else:
        print("Loại bài học này không hỗ trợ cập nhật qua tác vụ này.")
