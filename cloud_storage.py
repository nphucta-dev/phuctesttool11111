# -*- coding: utf-8 -*-
"""
cloud_storage.py
------------------
Minh họa kỹ thuật Duck Typing: AWSS3StorageService và
GoogleCloudStorageService là 2 lớp HOÀN TOÀN ĐỘC LẬP, không kế thừa từ
bất kỳ interface/abstract chung nào. Hàm sync_to_cloud() chỉ quan tâm đối
tượng truyền vào có phương thức upload_lesson(lesson) hay không.
"""


class AWSS3StorageService:
    """Dịch vụ lưu trữ AWS S3 - độc lập, không kế thừa BaseLesson hay interface nào."""

    def upload_lesson(self, lesson):
        print(f"[Hệ thống AWS S3]: Đang khởi tạo luồng băng thông kết nối tới LMS...")
        return True


class GoogleCloudStorageService:
    """Dịch vụ lưu trữ Google Cloud - độc lập, không kế thừa BaseLesson hay interface nào."""

    def upload_lesson(self, lesson):
        print(f"[Hệ thống Google Cloud]: Đang khởi tạo luồng băng thông kết nối tới LMS...")
        return True


def sync_to_cloud(cloud_service, lesson):
    """
    Hàm toàn cục độc lập, KHÔNG quan tâm cloud_service thuộc class nhà cung
    cấp nào (AWS, Google, Azure, Huawei...). Miễn là đối tượng truyền vào có
    hàm upload_lesson(lesson) thì hàm này hoạt động được -- tinh thần Duck
    Typing. Giúp tích hợp vô hạn nhà cung cấp cloud mới mà không cần sửa
    code ở lớp bài học gốc hay ở hàm này.

    Bẫy 4: nếu đối tượng truyền vào không có upload_lesson -> bắt AttributeError.
    """
    try:
        cloud_service.upload_lesson(lesson)
        print("Xác thực dịch vụ bằng Duck Typing thành công!")
        print(f"Hệ thống lưu trữ đám mây đã upload toàn bộ tài nguyên của bài học "
              f"{lesson.lesson_code} lên cụm máy chủ an toàn.")
    except AttributeError:
        print("Dịch vụ lưu trữ đám mây không hợp lệ hoặc chưa ký kết chứng chỉ API liên thông")
