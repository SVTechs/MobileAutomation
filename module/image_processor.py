import cv2
import numpy as np
from paddleocr import PaddleOCR
from .ocr_result import OCRResult
import threading

class ImageProcessor:
   _ocr = PaddleOCR(use_angle_cls=True, lang='ch',
                    det_model_dir='./assets/paddleModel/det',
                    rec_model_dir='./assets/paddleModel/rec',
                    cls_model_dir='./assets/paddleModel/cls',
                    show_log=False)
   _lock = threading.Lock()

   @classmethod
   def ocr_text(cls, image_stream):
       with cls._lock:
           results = cls._ocr.ocr(image_stream, cls=True)
           ocr_result_objects = []
           for result in results:
               for line in result:
                   coordinates, (text, confidence) = line
                   ocr_result_objects.append(OCRResult.from_paddleocr_result((coordinates, (text, confidence))))
           return ocr_result_objects