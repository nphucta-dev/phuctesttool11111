# -*- coding: utf-8 -*-
"""
lesson_models.py
------------------
Module định nghĩa toàn bộ các lớp bài học của hệ thống Rikkei E-Learning
Simulator Pro: lớp trừu tượng BaseLesson, các lớp con VideoLesson /
CodingChallenge, và lớp đa kế thừa kiểu "diamond" HybridAssessment.
"""

from abc import ABC, abstractmethod


class BaseLesson(ABC):
    """
    Lớp trừu tượng (Abstract Base Class) làm bộ khung chuẩn cho mọi bài học
    trên LMS. Không thể khởi tạo trực tiếp lớp này vì có chứa @abstractmethod
    (Bẫy 1: Python tự ném TypeError qua ABCMeta, không cần code thêm).
    """

    # Class Attributes: dùng chung toàn hệ thống
    platform_name = "Rikkei Academy LMS"
    base_completion_points = 10  # Điểm kinh nghiệm cơ bản (XP) / bài học

    def __init__(self, lesson_code, title, duration_minutes=0, **kwargs):
        self._lesson_code = lesson_code
        # Gọi qua property setter để tự động chuẩn hóa tiêu đề
        self.title = title
        # Private attribute (đóng gói thời lượng) -> _BaseLesson__duration_minutes
        self.__duration_minutes = duration_minutes
        # Cooperative super() theo MRO -- xem giải thích chi tiết ở HybridAssessment
        super().__init__(**kwargs)

    # ---------------------- PROPERTIES ----------------------
    @property
    def duration_minutes(self):
        """Chỉ cho đọc thời lượng bài học, không có setter để chặn thay đổi tùy tiện."""
        return self.__duration_minutes

    @property
    def lesson_code(self):
        return self._lesson_code

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Chuẩn hóa: xóa khoảng trắng thừa, in hoa
        self._title = " ".join(value.split()).upper()

    # ---------------------- PROTECTED HELPER ----------------------
    def _set_duration(self, minutes):
        """
        Vì __duration_minutes bị name-mangling (chỉ BaseLesson truy cập được),
        các lớp con và feature dùng phương thức bảo vệ này để thay đổi thời
        lượng, vẫn đảm bảo encapsulation (Bẫy 2: kiểm tra > 0 được thực hiện
        ở lớp gọi trước khi truyền vào đây).
        """
        self.__duration_minutes = minutes

    # ---------------------- ABSTRACT METHODS ----------------------
    @abstractmethod
    def calculate_completion_score(self):
        """Mỗi loại bài học phải tự định nghĩa công thức tính điểm XP (Đa hình)."""
        raise NotImplementedError

    @abstractmethod
    def update_content(self, new_data):
        """Mỗi loại bài học phải tự định nghĩa cách cập nhật nội dung (Đa hình)."""
        raise NotImplementedError

    # ---------------------- OPERATOR OVERLOADING ----------------------
    def __add__(self, other):
        """
        Nạp chồng toán tử +: cộng thời lượng của 2 bài học bất kỳ.
        Bẫy 3: nếu `other` không phải BaseLesson (str, int...) -> trả về
        NotImplemented để Python tự chuyển thành TypeError chuẩn.
        """
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes + other.duration_minutes

    def __lt__(self, other):
        """
        Nạp chồng toán tử <: so sánh thời lượng của 2 bài học.
        Bẫy 3: tương tự __add__, trả về NotImplemented nếu kiểu không hợp lệ.
        """
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes < other.duration_minutes

    # ---------------------- STATIC & CLASS METHOD ----------------------
    @staticmethod
    def validate_lesson_code(lesson_code):
        """
        Static method: logic kiểm tra hoàn toàn độc lập với trạng thái của
        đối tượng/lớp. Mã bài học phải là chuỗi đúng 10 ký tự và bắt đầu
        bằng "LMS" (ví dụ "LMS1234567").
        """
        return (
            isinstance(lesson_code, str)
            and len(lesson_code) == 10
            and lesson_code.startswith("LMS")
        )

    @classmethod
    def update_base_points(cls, new_points):
        """
        Class method: dùng cls để thay đổi Class Attribute `base_completion_points`,
        áp dụng cho toàn hệ thống (mọi bài học đều dùng chung điểm XP cơ sở).
        """
        cls.base_completion_points = new_points

    def __repr__(self):
        return f"{type(self).__name__}({self.lesson_code}, {self.title}, {self.duration_minutes}m)"


class VideoLesson(BaseLesson):
    """Bài học video lý thuyết: tính điểm theo thời lượng, đếm lượt xem."""

    def __init__(self, lesson_code, title, duration_minutes=0,
                 video_quality="1080p", view_count=0, **kwargs):
        self.video_quality = video_quality
        self.view_count = view_count
        # super().__init__() tái sử dụng logic lớp cha. Trong đa kế thừa
        # HybridAssessment, lệnh này đi theo MRO chứ không nhất thiết trỏ
        # thẳng tới BaseLesson.
        super().__init__(lesson_code, title, duration_minutes, **kwargs)

    def calculate_completion_score(self):
        """
        Ghi đè (override): điểm video = base_completion_points + duration_minutes * 0.5.
        Học viên xem bài học dài hơn được thưởng nhiều XP hơn.
        """
        return self.base_completion_points + self.duration_minutes * 0.5

    def update_content(self, new_data):
        """
        Ghi đè (override): cập nhật chất lượng video (ví dụ: "4K", "720p")
        hoặc tiêu đề bài học (nếu new_data là chuỗi không phải độ phân giải).
        Trả về mô tả nội dung đã cập nhật.
        """
        if new_data <= 0:
            raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")
        # Đối với VideoLesson, new_data số nguyên = cập nhật thời lượng (phút)
        self._set_duration(new_data)
        return new_data

    def play_video(self):
        """Giả lập học viên nhấn xem video: tăng view_count thêm 1 lượt."""
        self.view_count += 1


class CodingChallenge(BaseLesson):
    """Bài tập lập trình: tính điểm theo số testcase nhân hệ số độ khó."""

    def __init__(self, lesson_code, title, duration_minutes=0,
                 number_of_testcases=5, difficulty_multiplier=1.5, **kwargs):
        self.number_of_testcases = number_of_testcases
        self.difficulty_multiplier = difficulty_multiplier
        super().__init__(lesson_code, title, duration_minutes, **kwargs)

    def calculate_completion_score(self):
        """
        Ghi đè (override): điểm coding = base_completion_points * number_of_testcases
        * difficulty_multiplier. Bài khó (multiplier cao) + nhiều testcase = XP cao hơn.
        """
        return self.base_completion_points * self.number_of_testcases * self.difficulty_multiplier

    def update_content(self, new_data):
        """
        Ghi đè (override): thay đổi số lượng testcase cho bài tập.
        Bẫy 2: new_data phải > 0.
        """
        if new_data <= 0:
            raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")
        self.number_of_testcases = new_data
        return new_data


class HybridAssessment(VideoLesson, CodingChallenge):
    """
    Bài kiểm tra tổng hợp cuối module: đa kế thừa (Multiple Inheritance)
    kiểu "diamond" từ CẢ VideoLesson VÀ CodingChallenge -- cả hai đều kế
    thừa từ BaseLesson.

    MRO (Method Resolution Order) theo C3-linearization của Python:
        HybridAssessment -> VideoLesson -> CodingChallenge -> BaseLesson -> ABC -> object
    Kiểm tra trực tiếp bằng HybridAssessment.__mro__.

    XUNG ĐỘT PHƯƠNG THỨC: cả VideoLesson và CodingChallenge đều định nghĩa
    calculate_completion_score() và update_content() với công thức/hành vi
    khác nhau. Nếu HybridAssessment không tự override, Python chọn phiên
    bản của VideoLesson (đứng trước trong MRO) cho cả hai -- điều này SAI
    vì HybridAssessment cần kết hợp ĐỒNG THỜI điểm theo thời lượng video
    LẪN điểm theo số testcase độ khó.

    KHỞI TẠO cooperative: super().__init__(**kwargs) đi theo MRO:
        HybridAssessment -> VideoLesson -> CodingChallenge -> BaseLesson
    đảm bảo cả video_quality, view_count (VideoLesson) và
    number_of_testcases, difficulty_multiplier (CodingChallenge) đều được
    gán đầy đủ chỉ với một lệnh super().__init__() duy nhất.
    """

    def __init__(self, lesson_code, title, duration_minutes=0,
                 video_quality="1080p", view_count=0,
                 number_of_testcases=5, difficulty_multiplier=1.5):
        super().__init__(
            lesson_code, title, duration_minutes,
            video_quality=video_quality,
            view_count=view_count,
            number_of_testcases=number_of_testcases,
            difficulty_multiplier=difficulty_multiplier,
        )

    def calculate_completion_score(self):
        """
        Giải quyết xung đột: HybridAssessment kết hợp ĐỒNG THỜI:
          - Điểm video (VideoLesson): base + duration * 0.5
          - Điểm coding (CodingChallenge): base * testcases * multiplier
        Công thức tổng hợp (trừ 1 lần base để tránh đếm điểm cơ sở 2 lần):
          score = VideoLesson_score + CodingChallenge_score - base
                = (base + duration*0.5) + (base*testcases*multiplier) - base
                = base + duration*0.5 + base*testcases*multiplier
        Với base=10, duration=45, testcases=8, multiplier=1.5:
          = 10 + 22.5 + 120 = 152.5 XP
        """
        video_score = VideoLesson.calculate_completion_score(self)
        coding_score = CodingChallenge.calculate_completion_score(self)
        # Trừ base_completion_points một lần để không tính double base
        return video_score + coding_score - self.base_completion_points

    def update_content(self, new_data):
        """
        Giải quyết xung đột: HybridAssessment update_content cập nhật
        number_of_testcases (hành vi CodingChallenge) -- gọi đích danh
        CodingChallenge.update_content thay vì để MRO tự chọn VideoLesson.
        """
        return CodingChallenge.update_content(self, new_data)


if __name__ == "__main__":
    # Demo nhanh Bẫy 1
    try:
        BaseLesson("LMS0000001", "test")
    except TypeError as e:
        print(f"[Bẫy 1 - OK] {e}")

    print("\nMRO của HybridAssessment:")
    for cls in HybridAssessment.__mro__:
        print(" ->", cls.__name__)

    h = HybridAssessment("LMS0012345", "  huong dan oop python  ",
                          duration_minutes=45, video_quality="1080p",
                          number_of_testcases=8, difficulty_multiplier=1.5)
    print(f"\nHybrid score: {h.calculate_completion_score()} XP")
    print(f"video_quality: {h.video_quality}")
    print(f"number_of_testcases: {h.number_of_testcases}")
    print(f"title: {h.title}")
