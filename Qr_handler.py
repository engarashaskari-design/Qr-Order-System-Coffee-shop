import qrcode
from PIL import Image
import cv2
import numpy as np
import json
import uuid

class QRHandler:
    @staticmethod
    def generate_order_qr(order_code, table_number=None, amount=None):
        data = {
            "order_code": order_code,
            "type": "order",
            "timestamp": str(uuid.uuid4())[:8],
            "table": table_number,
            "amount": amount
        }
        
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        qr.add_data(json.dumps(data))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"qr_{order_code}.png")
        return f"qr_{order_code}.png"
    
    @staticmethod
    def scan_qr_from_camera():
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        
        print("🔍 Camera activated - Press Q to exit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            data, points, _ = detector.detectAndDecode(frame)
            
            if data:
                if points is not None:
                    points = points.astype(int)
                    cv2.polylines(frame, [points], True, (0,255,0), 3)
                
                cv2.putText(frame, "✓ Scanned!", (50,50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                cap.release()
                cv2.destroyAllWindows()
                return json.loads(data)
            
            cv2.imshow('QR Scanner', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return None
