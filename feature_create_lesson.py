# -*- coding: utf-8 -*-
"""
feature_create_lesson.py
--------------------------
Chức năng 1: Khởi tạo bài học mới (VideoLesson / CodingChallenge / HybridAssessment).
"""

from lesson_models import BaseLesson, VideoLesson, CodingChallenge, HybridAssessment
from utils import parse_number


def feature1_create_lesson(lessons):
    """
    Tạo và thêm một bài học mới vào danh sách `lessons`.
    Trả về đối tượng bài học mới (để main.py gán làm current_lesson),
    hoặc None nếu khởi tạo thất bại.
    """
    print("\n--- CHỌN LOẠI BÀI HỌC KHỞI TẠO ---")
    print("1. Video Lesson (Bài học Video Lý Thuyết)")
    print("2. Coding Challenge (Bài tập Thực Hành Code)")
    print("3. Hybrid Assessment (Bài Kiểm Tra Tổng Hợp)")
    lesson_type = input("Chọn loại bài học (1-3): ").strip()

    if lesson_type not in ("1", "2", "3"):
        print("\nLoại bài học không hợp lệ!")
        return None

    lesson_code = input("Nhập mã bài học 10 ký tự: ").strip()
    # Bẫy: mã bài học phải đúng 10 ký tự và bắt đầu bằng "LMS" -> @staticmethod
    if not BaseLesson.validate_lesson_code(lesson_code):
        print("Mã bài học không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng LMS.")
        return None

    if any(l.lesson_code == lesson_code for l in lessons):
        print("Mã bài học đã tồn tại trong hệ thống!")
        return None

    title_raw = input("Nhập tiêu đề bài học: ")

    try:
        duration = int(parse_number(input("Nhập thời lượng bài học (phút): ").strip()))
        if duration <= 0:
            print("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")
            return None

        if lesson_type == "1":
            quality = input("Nhập chất lượng video (ví dụ 1080p): ").strip() or "1080p"
            new_lesson = VideoLesson(lesson_code, title_raw, duration_minutes=duration,
                                     video_quality=quality)
            print("\nKhởi tạo bài học Video thành công!")

        elif lesson_type == "2":
            testcases = int(parse_number(input("Nhập số lượng testcase: ").strip()))
            multiplier = float(parse_number(input("Nhập hệ số độ khó (ví dụ 1.5): ").strip()))
            new_lesson = CodingChallenge(lesson_code, title_raw, duration_minutes=duration,
                                          number_of_testcases=testcases,
                                          difficulty_multiplier=multiplier)
            print("\nKhởi tạo bài học Coding Challenge thành công!")

        else:  # lesson_type == "3"
            quality = input("Nhập chất lượng video (ví dụ 1080p): ").strip() or "1080p"
            testcases = int(parse_number(input("Nhập số lượng testcase: ").strip()))
            multiplier = float(parse_number(input("Nhập hệ số độ khó (ví dụ 1.5): ").strip()))
            new_lesson = HybridAssessment(lesson_code, title_raw, duration_minutes=duration,
                                           video_quality=quality,
                                           number_of_testcases=testcases,
                                           difficulty_multiplier=multiplier)
            print("\nKhởi tạo bài học Hybrid Assessment thành công!")

    except ValueError as e:
        print(f"Dữ liệu nhập không hợp lệ: {e}")
        return None

    lessons.append(new_lesson)
    print(f"Tiêu đề bài học: {new_lesson.title}")
    return new_lesson
