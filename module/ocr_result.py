class OCRResult:
    def __init__(self, text, confidence, rec):
        self.text = text
        self.confidence = confidence
        self.rec = rec

    @classmethod
    def from_paddleocr_result(cls, result):
        coordinates = result[0]
        text, confidence = result[1]

        x1, y1 = coordinates[0][0], coordinates[0][1]
        x2, y2 = coordinates[1][0], coordinates[1][1]
        x3, y3 = coordinates[2][0], coordinates[2][1]
        x4, y4 = coordinates[3][0], coordinates[3][1]

        # 根据坐标计算左上角和右下角的坐标
        upper_left_x = min(x1, x2, x3, x4)
        upper_left_y = min(y1, y2, y3, y4)
        bottom_right_x = max(x1, x2, x3, x4)
        bottom_right_y = max(y1, y2, y3, y4)

        # 创建rec列表，包含左上角和右下角坐标
        rec = [upper_left_x, upper_left_y, bottom_right_x, bottom_right_y]

        return cls(text, confidence, rec)

    @classmethod
    def from_cnocr_result(cls, result):
        text = result['text']
        confidence = result['score']
        position = result['position']

        # 提取坐标
        x1, y1 = position[0][0], position[0][1]
        x2, y2 = position[1][0], position[1][1]
        x3, y3 = position[2][0], position[2][1]
        x4, y4 = position[3][0], position[3][1]

        # 根据坐标计算左上角和右下角的坐标
        upper_left_x = min(x1, x2, x3, x4)
        upper_left_y = min(y1, y2, y3, y4)
        bottom_right_x = max(x1, x2, x3, x4)
        bottom_right_y = max(y1, y2, y3, y4)

        # 创建rec列表，包含左上角和右下角坐标
        rec = [upper_left_x, upper_left_y, bottom_right_x, bottom_right_y]

        return cls(text, confidence, rec)

    def __repr__(self):
        return f"OCRResult(text='{self.text}', confidence={self.confidence}, rec={self.rec})"