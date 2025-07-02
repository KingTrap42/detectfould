import cv2
import numpy as np
import os

# TODO: Ganti dengan path model SSD yang sudah dilatih
MODEL_PATH = '../models/ssd_model/model.pth'

# TODO: Ganti dengan label yang sesuai dengan dataset
CLASS_NAMES = ['person', 'shuttlecock', 'racket', 'service_line']

# Fungsi untuk load model SSD (dummy, ganti dengan load model sebenarnya)
def load_ssd_model(model_path):
    # Placeholder: ganti dengan kode load model SSD sebenarnya
    print(f"Model SSD diload dari {model_path}")
    model = None
    return model

# Fungsi untuk deteksi objek pada frame (dummy, ganti dengan prediksi model sebenarnya)
def detect_objects(model, frame):
    # Placeholder: return list of dict {'label': str, 'bbox': [x1, y1, x2, y2], 'score': float}
    # Contoh: [{'label': 'person', 'bbox': [100,200,150,300], 'score': 0.9}, ...]
    return []

# Fungsi untuk cek pelanggaran service
# Kriteria: kaki menyentuh garis sebelum kok dipukul
def check_service_violation(detections, violation_state):
    # violation_state: dict untuk menyimpan status pelanggaran antar frame
    # Return: is_violation (bool), updated violation_state
    # TODO: Implementasi logika deteksi pelanggaran
    is_violation = False
    # ...
    return is_violation, violation_state

# Fungsi untuk visualisasi hasil deteksi dan notifikasi
def visualize(frame, detections, is_violation):
    for det in detections:
        label = det['label']
        bbox = det['bbox']
        score = det['score']
        x1, y1, x2, y2 = bbox
        color = (0,255,0) if label != 'service_line' else (255,0,0)
        cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
        cv2.putText(frame, f"{label} {score:.2f}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    if is_violation:
        cv2.putText(frame, 'Pelanggaran Service!', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)
    return frame

def main(video_path, output_path=None):
    model = load_ssd_model(MODEL_PATH)
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None
    if output_path:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    violation_state = {}
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        detections = detect_objects(model, frame)
        is_violation, violation_state = check_service_violation(detections, violation_state)
        vis_frame = visualize(frame, detections, is_violation)
        cv2.imshow('Deteksi Pelanggaran Service', vis_frame)
        if out:
            out.write(vis_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Deteksi Pelanggaran Service Bulutangkis')
    parser.add_argument('--video', type=str, required=True, help='Path ke file video input')
    parser.add_argument('--output', type=str, default=None, help='Path untuk menyimpan video output (opsional)')
    args = parser.parse_args()
    main(args.video, args.output) 