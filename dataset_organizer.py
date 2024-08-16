import os
import shutil
import random

def write_to_txt_files(path, content):

    for root, dirs, files in os.walk(path):
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            txt_file_path = os.path.join(root, file_name + '.txt')
            with open(txt_file_path, 'w') as txt_file:
                txt_file.write(content)
                print(f"{txt_file_path} dosyasına yazıldı.")

def copy_files_to_directory(source_dir, destination_dir):

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        destination_path = os.path.join(destination_dir, item)
        
        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
            print(f"{source_path} -> {destination_path} kopyalandı.")
        else:
            print(f"{source_path} bir dosya değil, atlanıyor.")


def move_txt_files(source_dir, destination_dir):
    # Hedef klasörün var olduğundan emin olun, yoksa oluşturun
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    # Kaynak klasördeki tüm dosyaları gez
    for file in os.listdir(source_dir):
        source_path = os.path.join(source_dir, file)
        destination_path = os.path.join(destination_dir, file)
        
        # Eğer dosya .txt uzantılı ise taşır
        if os.path.isfile(source_path) and file.endswith('.txt'):
            shutil.move(source_path, destination_path)
            print(f"{source_path} -> {destination_path} taşındı.")
        else:
            print(f"{file} bir .txt dosyası değil, atlanıyor.")

def move_images(source_dir, destination_dir):

    # Hedef klasörün var olduğundan emin olun, yoksa oluşturun
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    # Kaynak klasördeki tüm dosyaları gez
    for file in os.listdir(source_dir):
        source_path = os.path.join(source_dir, file)
        destination_path = os.path.join(destination_dir, file)
        
        # Eğer dosya .txt uzantılı ise taşır
        if os.path.isfile(source_path) and file.endswith('.jpg'):
            shutil.move(source_path, destination_path)
            print(f"{source_path} -> {destination_path} taşındı.")
        else:
            print(f"{file} bir .txt dosyası değil, atlanıyor.")

def split_files_into_sets(source_dir, train_dir, test_dir, valid_dir, train_ratio=0.7, test_ratio=0.1, valid_ratio=0.2):

    files = os.listdir(source_dir)
    
    file_groups = {}
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        if file_name not in file_groups:
            file_groups[file_name] = []
        file_groups[file_name].append(file)
    
    file_groups = list(file_groups.values())
    random.shuffle(file_groups)
    
    total_groups = len(file_groups)
    train_count = int(total_groups * train_ratio)
    test_count = int(total_groups * test_ratio)
    valid_count = total_groups - train_count - test_count
    
    train_files = file_groups[:train_count]
    test_files = file_groups[train_count:train_count + test_count]
    valid_files = file_groups[train_count + test_count:]
    
    for group in train_files:
        for file in group:
            shutil.copy2(os.path.join(source_dir, file), os.path.join(train_dir, file))
    
    for group in test_files:
        for file in group:
            shutil.copy2(os.path.join(source_dir, file), os.path.join(test_dir, file))
    
    for group in valid_files:
        for file in group:
            shutil.copy2(os.path.join(source_dir, file), os.path.join(valid_dir, file))
    print("Splitted into train, valid and test sets.")

# Kullanım örnekleri
source_directory = '/home/utku/Desktop/BIL476/clustered_images/cluster_1'  # Buraya kaynak klasörün yolunu girin
train_directory = '/home/utku/BIL476/dataGreen/train'  # Buraya train klasörünün yolunu girin
test_directory = '/home/utku/BIL476/dataGreen/test'  # Buraya test klasörünün yolunu girin
valid_directory = '/home/utku/BIL476/dataGreen/valid'  # Buraya valid klasörünün yolunu girin
team_directory = '/home/utku/BIL476/arsenal'
dataset_directory = '/home/utku/BIL476/datasetGreen'

# Hedef klasörlerin var olduğundan emin olun, yoksa oluşturun
os.makedirs(train_directory, exist_ok=True)
os.makedirs(test_directory, exist_ok=True)
os.makedirs(valid_directory, exist_ok=True)
os.makedirs(team_directory, exist_ok=True)
os.makedirs(dataset_directory, exist_ok=True)

# Belirtilen pathteki dosyalarla aynı isime sahip .txt dosyaları oluşturup içerik yazma
# write_to_txt_files(total_directory, '1 0.500000 0.500000 1.000000 1.000000')

# Dosyaları train, test ve valid setlerine ayırma
split_files_into_sets(dataset_directory, train_directory, test_directory, valid_directory)

move_txt_files(train_directory, '/home/utku/BIL476/dataGreen/train/labels')
move_images(train_directory, '/home/utku/BIL476/dataGreen/train/images')

move_txt_files(valid_directory, '/home/utku/BIL476/dataGreen/valid/labels')
move_images(valid_directory, '/home/utku/BIL476/dataGreen/valid/images')

move_txt_files(test_directory, '/home/utku/BIL476/dataGreen/test/labels')
move_images(test_directory, '/home/utku/BIL476/dataGreen/test/images')


# Kaynak klasördeki tüm dosyaları hedef klasöre kopyalama
# copy_files_to_directory(team_directory, dataset_directory)

