import cv2
import os
import numpy as np

input_dir = '/home/utku/BIL476/arsenal'  # Orijinal resimlerin olduğu dizin
output_dir = '/home/utku/BIL476/arsenal'  # Yeni resimlerin kaydedileceği dizin

target_size = (1280, 720)

# Futbol sahası yeşili için RGB renk değeri (örneğin)
background_color = (34, 139, 34)  # Bu rengi resme göre ayarlayabilirsiniz

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        img_path = os.path.join(input_dir, filename)
        img = cv2.imread(img_path)
        
        # Orijinal görüntü boyutlarını al
        original_height, original_width = img.shape[:2]
        
        # Eğer orijinal görüntü hedef boyuttan büyükse, yeniden boyutlandır
        if original_height > target_size[1] or original_width > target_size[0]:
            scaling_factor = min(target_size[1] / original_height, target_size[0] / original_width)
            img = cv2.resize(img, (int(original_width * scaling_factor), int(original_height * scaling_factor)))
            original_height, original_width = img.shape[:2]
        
        # Yeni görüntüyü futbol sahası yeşili (background_color) ile doldur
        padded_img = np.full((target_size[1], target_size[0], 3), background_color, dtype=np.uint8)
        
        # Orijinal görüntüyü sol üst köşeye yerleştir
        padded_img[:original_height, :original_width] = img
        
        # Yeni görüntüyü kaydet
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, padded_img)
        
        # Bounding box'u ayarla
        x_center = (original_width / 2) / target_size[0]
        y_center = (original_height / 2) / target_size[1]
        width = original_width / target_size[0]
        height = original_height / target_size[1]
        
        bbox = [x_center, y_center, width, height]
        
        print(f"Processed {filename}: Bounding Box: {bbox}")
        
        # Bounding box'u bir dosyaya yaz (örnek olarak .txt dosyasına yazıyoruz)
        bbox_path = os.path.splitext(output_path)[0] + '.txt'
        with open(bbox_path, 'w') as f:
            f.write('0 ' + ' '.join(map(str, bbox)) + '\n')  # '0' sınıf etiketi olarak kullanıldı

print("All images have been padded and bounding boxes calculated.")