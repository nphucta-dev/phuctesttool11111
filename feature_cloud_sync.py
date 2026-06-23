# -*- coding: utf-8 -*-
"""
feature_cloud_sync.py
-----------------------
Chức năng 6: Đồng bộ bài giảng lên Nền tảng Đám mây (Duck Typing).
"""

from cloud_storage import AWSS3StorageService, GoogleCloudStorageService, sync_to_cloud


def feature6_cloud_sync(current_lesson):
    if current_lesson is None:
        print("\nVui lòng khởi tạo/chọn bài học trước khi đồng bộ đám mây.")
        return

    print("\n--- ĐỒNG BỘ BÀI GIẢNG LÊN NỀN TẢNG ĐÁM MÂY ---")
    print("1. Đồng bộ lên máy chủ AWS S3 Storage")
    print("2. Đồng bộ lên máy chủ Google Cloud Storage")
    choice = input("Chọn dịch vụ lưu trữ (1-2): ").strip()

    if choice == "1":
        service = AWSS3StorageService()
    elif choice == "2":
        service = GoogleCloudStorageService()
    else:
        print("Dịch vụ lưu trữ không hợp lệ!")
        return

    # sync_to_cloud không quan tâm `service` thuộc class nào (Duck Typing).
    # Bẫy 4 (AttributeError) được xử lý bên trong sync_to_cloud() nếu
    # service thiếu phương thức upload_lesson.
    sync_to_cloud(service, current_lesson)
