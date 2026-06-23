# -*- coding: utf-8 -*-
"""
feature_completion_score.py
-----------------------------
Chức năng 4: Xem chi tiết điểm thưởng hoàn thành bài học.

Gọi phương thức đa hình calculate_completion_score() của đối tượng hiện
tại để tính điểm XP thực tế học viên nhận được.
"""

from lesson_models import VideoLesson, CodingChallenge, HybridAssessment


def feature4_completion_score(current_lesson):
    if current_lesson is None:
        print("\nHệ thống chưa có bài học nào được chọn.")
        return

    print("\n--- CHI TIẾT ĐIỂM THƯỞNG HOÀN THÀNH ---")
    print(f"Bài học: {current_lesson.title} (Loại: {type(current_lesson).__name__})")
    print(f"Điểm cơ sở hệ thống: {current_lesson.base_completion_points} XP")
    print(f"Thời lượng tích lũy: {current_lesson.duration_minutes} phút")

    # Hiển thị chi tiết thành phần tính điểm theo loại (đa hình về thuộc tính)
    if isinstance(current_lesson, HybridAssessment):
        print(f"Số lượng testcase cấu hình: {current_lesson.number_of_testcases} bài")
        print(f"Hệ số độ khó: {current_lesson.difficulty_multiplier}")
    elif isinstance(current_lesson, CodingChallenge):
        print(f"Số lượng testcase cấu hình: {current_lesson.number_of_testcases} bài")
        print(f"Hệ số độ khó: {current_lesson.difficulty_multiplier}")
    elif isinstance(current_lesson, VideoLesson):
        print(f"Chất lượng video: {current_lesson.video_quality}")

    # Đa hình: calculate_completion_score() tự chọn đúng công thức theo lớp
    score = current_lesson.calculate_completion_score()
    print(f"Tổng điểm kinh nghiệm (XP) nhận được khi hoàn thành: {score:g} XP")

    return score
