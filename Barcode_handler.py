from barcode import EAN13
from barcode.writer import ImageWriter
from PIL import Image
import cv2
import numpy as np
from pyzbar.pyzbar import decode

class BarcodeHandler:
    @staticmethod
    def generate_barcode(product_code, filename="product_barcode"):
        full_code = str(product_code).zfill(12) + "0"
        
        try:
            ean = EAN13(full_code, writer=ImageWriter())
            ean.save(filename)
            return f"{filename}.png"
        except Exception as e:
            print(f"Barcode generation error: {e}")
            return None
    
    @staticmethod
    def scan_barcode_from_image(image_path):
        img = Image.open(image_path)
        decoded_objects = decode(img)
        
        for obj in decoded_objects:
            return obj.data.decode('utf-8')
        return None
    
    @staticmethod
    def scan_barcode_from_camera():
        cap = cv2.VideoCapture(0)
        print("📷 Camera activated for barcode scanning - Press Q to exit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            barcodes = decode(frame)
            
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                barcode_type = barcode.type
                
                points = barcode.polygon
                if points:
                    pts = [(point.x, point.y) for point in points]
                    cv2.polylines(frame, [np.array(pts, np.int32)], True, (0,255,0), 2)
                
                cv2.putText(frame, f"{barcode_data} ({barcode_type})", 
                           (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                
                cap.release()
                cv2.destroyAllWindows()
                return barcode_data
            
            cv2.imshow('Barcode Scanner', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return None
