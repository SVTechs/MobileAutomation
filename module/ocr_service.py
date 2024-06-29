import zerorpc
import cv2
import numpy as np
from paddleocr import PaddleOCR
from .ocr_result import OCRResult
import logging
import threading

class OcrService(object):
    _instance = None
    _server = None
    _port = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(OcrService, cls).__new__(cls)
        return cls._instance

    def __init__(self, port=4242):
        if not hasattr(self, '_initialized'):
            self._ocr = PaddleOCR(use_angle_cls=True, lang='ch',
                                  det_model_dir='./assets/paddleModel/det',
                                  rec_model_dir='./assets/paddleModel/rec',
                                  cls_model_dir='./assets/paddleModel/cls',
                                  show_log=True)
            self._port = port
            self._initialized = True
            self._logger = logging.getLogger(__name__)
            self._logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def ocr_text(self, image_data):
        try:
            results = self._ocr.ocr(image_data, cls=True)
            ocr_result_objects = []
            for result in results:
                for line in result:
                    coordinates, (text, confidence) = line
                    ocr_result_objects.append(OCRResult.from_paddleocr_result((coordinates, (text, confidence))))
            return [obj.__dict__ for obj in ocr_result_objects]
        except Exception as e:
            self._logger.error(f"Error during OCR processing: {e}")
            return []

    def start(self):
        if self._server is not None:
            self._logger.info("Server is already running.")
            return
        self._server = zerorpc.Server(self)
        self._server.bind(f"tcp://127.0.0.1:{self._port}")
        threading.Thread(target=self._server.run).start()
        self._logger.info("Server started.")

    def stop(self):
        if self._server is not None:
            self._server.stop()
            self._server = None
            self._logger.info("Server stopped.")
        else:
            self._logger.info("Server is not running.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    service = OcrService(port=4242)
    service.start()