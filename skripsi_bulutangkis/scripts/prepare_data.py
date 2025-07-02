# scripts/prepare_data.py
import os
import xml.etree.ElementTree as ET
import random
import shutil

def parse_voc_annotation(annotation_path):
    """
    Parse XML annotation file (Pascal VOC format).
    Returns a list of dictionaries, each containing:
    {
        'box': [xmin, ymin, xmax, ymax],
        'label': 'class_name'
    }
    """
    tree = ET.parse(annotation_path)
    root = tree.getroot()
    boxes = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        boxes.append({
            'box': [xmin, ymin, xmax, ymax],
            'label': name
        })
    return boxes

def split_dataset(image_dir, annotation_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """
    Splits the dataset into training, validation, and test sets.
    """
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(image_files)

    num_total = len(image_files)
    num_train = int(num_total * train_ratio)
    num_val = int(num_total * val_ratio)

    train_files = image_files[:num_train]
    val_files = image_files[num_train:num_train + num_val]
    test_files = image_files[num_train + num_val:]

    # Create directories
    os.makedirs(os.path.join(DATA_DIR, 'train', 'images'), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'train', 'annotations'), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'val', 'images'), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'val', 'annotations'), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'test', 'images'), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'test', 'annotations'), exist_ok=True)

    def copy_files(file_list, src_img_dir, src_annot_dir, dest_img_dir, dest_annot_dir):
        for f in file_list:
            img_src_path = os.path.join(src_img_dir, f)
            annot_src_path = os.path.join(src_annot_dir, os.path.splitext(f)[0] + '.xml') # Assuming XML annotations
            
            if os.path.exists(annot_src_path):
                shutil.copy(img_src_path, dest_img_dir)
                shutil.copy(annot_src_path, dest_annot_dir)
            else:
                print(f"Warning: Annotation file for {f} not found. Skipping.")

    print(f"Copying {len(train_files)} training files...")
    copy_files(train_files, image_dir, annotation_dir, TRAIN_IMG_DIR, TRAIN_ANNOT_DIR)
    print(f"Copying {len(val_files)} validation files...")
    copy_files(val_files, image_dir, annotation_dir, VAL_IMG_DIR, VAL_ANNOT_DIR)
    print(f"Copying {len(test_files)} test files...")
    copy_files(test_files, image_dir, annotation_dir, TEST_IMG_DIR, TEST_ANNOT_DIR)

    print("Dataset split complete.")

if __name__ == "__main__":
    from config import DATA_DIR, TRAIN_IMG_DIR, TRAIN_ANNOT_DIR, VAL_IMG_DIR, VAL_ANNOT_DIR, TEST_IMG_DIR, TEST_ANNOT_DIR

    # Pastikan Anda memiliki direktori 'raw_data/images' dan 'raw_data/annotations'
    # yang berisi semua gambar dan anotasi asli Anda sebelum menjalankan ini.
    RAW_IMAGE_DIR = 'raw_data/images' # Ubah ini ke direktori gambar asli Anda
    RAW_ANNOTATION_DIR = 'raw_data/annotations' # Ubah ini ke direktori anotasi asli Anda

    if not os.path.exists(RAW_IMAGE_DIR) or not os.path.exists(RAW_ANNOTATION_DIR):
        print(f"Error: Make sure '{RAW_IMAGE_DIR}' and '{RAW_ANNOTATION_DIR}' exist and contain your data.")
        print("Please put all your images in 'raw_data/images' and their corresponding XML annotations in 'raw_data/annotations'.")
    else:
        split_dataset(RAW_IMAGE_DIR, RAW_ANNOTATION_DIR)