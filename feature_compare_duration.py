# -*- coding: utf-8 -*-
"""
feature_compare_duration.py
-----------------------------
Chức năng 5: Kiểm tra gộp thời lượng & So sánh độ dài bài học (Operator Overloading).
"""


def feature5_compare_duration(lessons, current_lesson):
    if current_lesson is None:
        print("\nVui lòng khởi tạo/chọn bài học hiện tại trước (Chức năng 1).")
        return

    others = [l for l in lessons if l is not current_lesson]
    if not others:
        print("\nHệ thống chưa có bài học khác để so sánh/gộp thời lượng.")
        return

    print("\n--- ĐỒNG BỘ & SO SÁNH THỜI LƯỢNG (OPERATOR OVERLOADING) ---")
    print(f"Bài học hiện tại (A): {current_lesson.title} (Thời lượng: {current_lesson.duration_minutes} phút)")
    print("Danh sách bài học khác trong hệ thống:")
    for idx, l in enumerate(others, start=1):
        print(f"{idx}. {l.lesson_code} - {l.title} (Thời lượng: {l.duration_minutes} phút)")

    choice = input("Chọn bài học đối ứng (B) theo số thứ tự: ").strip()
    try:
        target = others[int(choice) - 1]
    except (ValueError, IndexError):
        print("Lựa chọn không hợp lệ!")
        return

    print(f"Bài học đối ứng (B): {target.title} (Thời lượng: {target.duration_minutes} phút)")

    # --- Toán tử __lt__ (Bẫy 3: nếu kiểu không hợp lệ, Python ném TypeError
    # vì __lt__ trả về NotImplemented khi không phải BaseLesson) ---
    try:
        if current_lesson < target:
            print("[Kết quả So sánh (__lt__)]: Thời lượng bài học A NGẮN HƠN thời lượng bài học B.")
        else:
            print("[Kết quả So sánh (__lt__)]: Thời lượng bài học A DÀI HƠN HOẶC BẰNG thời lượng bài học B.")
    except TypeError:
        print("[Kết quả So sánh (__lt__)]: Không thể so sánh (kiểu dữ liệu không hợp lệ).")

    # --- Toán tử __add__ ---
    try:
        total = current_lesson + target
        print(f"[Kết quả Tổng hợp (__add__)]: Tổng thời lượng học tập của cả 2 bài học là: {total:g} phút.")
    except TypeError:
        print("[Kết quả Tổng hợp (__add__)]: Không thể cộng (kiểu dữ liệu không hợp lệ).")
