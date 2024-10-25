import pymysql
import cv2
from datetime import datetime

def scan_qr_from_camera():
    cap = cv2.VideoCapture(0)  # 0 is the default camera, change if needed

    qr_data = None  # Placeholder for the QR data
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Decode QR codes
        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            # Get the QR code data found
            qr_data = data
            break  # Exit the loop once we have the QR data

        # Show the camera feed (optional)
        cv2.imshow('QR Code Scanner', frame)

        # Press 'q' to manually quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

    return qr_data

def fetch_customer_data(customer_id):
    connection = pymysql.connect(host='localhost', user='root', password='qwerty1234@#', database='Users')
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE customer_id = %s"
            cursor.execute(query, (customer_id,))
            column_names = [desc[0] for desc in cursor.description]
            row_data = cursor.fetchone()

            if row_data:
                data_dict = dict(zip(column_names, row_data))
                
                # Update entry_time
                update_query = "UPDATE users SET entry_time = %s WHERE customer_id = %s"
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(update_query, (current_time, customer_id))
                connection.commit()

                return data_dict
            else:
                return None
    finally:
        connection.close()