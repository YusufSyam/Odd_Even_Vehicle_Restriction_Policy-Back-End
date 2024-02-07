import os
import cv2

def delete_image_if_exists(image_dir, image_name):
    file_path= f'{os.path.join(image_dir, image_name)}'
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"File {file_path} berhasil dihapus.")
        except OSError as e:
            print(f"Gagal menghapus file {file_path}: {e}")
    else:
        print(f"File {file_path} tidak ditemukan dalam direktori.")


def decode_and_save_image(encoded_image_str, image_name, base_path):
    try:
        image_data = decode_image(encoded_image_str)
        
        save_image(image_data, image_name, base_path)
    except:
        print('Terjadi Kesalahan dalam Mendekode dan Menyimpan Gambar')

def decode_image(encoded_image_str):
    image_data = base64.b64decode(encoded_image_str)
    
    return image_data

def save_image(image_data, image_name, base_path):
    image_path = f"{base_path}/{image_name}"

    with open(image_path, "wb") as image:
        image.write(image_data)

def save_image_cv(image_data, image_name, base_path):
    image_path = f"{base_path}/{image_name}"
    cv2.imwrite(image_path, image_data)