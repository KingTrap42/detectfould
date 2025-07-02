# config.py

import os

# Path ke dataset
DATA_DIR = 'data/'
TRAIN_IMG_DIR = os.path.join(DATA_DIR, 'train', 'images')
TRAIN_ANNOT_DIR = os.path.join(DATA_DIR, 'train', 'annotations')
VAL_IMG_DIR = os.path.join(DATA_DIR, 'val', 'images')
VAL_ANNOT_DIR = os.path.join(DATA_DIR, 'val', 'annotations')
TEST_IMG_DIR = os.path.join(DATA_DIR, 'test', 'images')
TEST_ANNOT_DIR = os.path.join(DATA_DIR, 'test', 'annotations')

# Path untuk menyimpan model
MODEL_SAVE_PATH = 'models/ssd_model/'

# Parameter pelatihan
NUM_CLASSES = 3 # Contoh: 1 (pemain), 2 (raket), 3 (kok), 4 (area terlarang)
                # Sesuaikan dengan "tindakan kecurangan" yang ingin dideteksi sebagai objek
BATCH_SIZE = 8
LEARNING_RATE = 0.001
EPOCHS = 50 # Sesuaikan
IMAGE_SIZE = (300, 300) # Ukuran input untuk model SSD
SAVE_FREQ = 5 # Simpan model setiap N epoch

# Kelas yang akan dideteksi
# Contoh:
# Jika Anda mendeteksi "servis ilegal", Anda mungkin perlu mendeteksi objek seperti:
# 'pemain_servis', 'tangan_pemain', 'raket', 'kok', 'garis_servis'
# Dan kemudian menggunakan logika tambahan untuk menentukan kecurangan dari posisi relatif objek-objek tersebut.
# Atau Anda bisa melabeli langsung "servis_ilegal" sebagai satu kelas jika data Anda memungkinkan.
# Ini adalah tantangan besar dalam definisi dataset Anda.
LABELS = {
    'pemain': 0,
    'raket': 1,
    'kok': 2,
    'area_larangan_servis': 3, # Contoh objek yang dapat membantu deteksi
    # 'servis_ilegal': 4, # Jika Anda bisa mendapatkan anotasi langsung untuk kecurangan
}
REVERSE_LABELS = {v: k for k, v in LABELS.items()}

# Parameter deteksi
CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4

# Path ke model pre-trained (jika digunakan)
# PRETRAINED_MODEL_PATH = 'path/to/pretrained/ssd_mobilenet_v2_coco/checkpoint/'