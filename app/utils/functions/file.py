from app.utils.const.const import IMAGE_FOLDER
import os

def delete_image_if_exists(image_name):
    file_path= f'{os.path.join(IMAGE_FOLDER, image_name)}'
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"File {file_path} berhasil dihapus.")
        except OSError as e:
            print(f"Gagal menghapus file {file_path}: {e}")
    else:
        print(f"File {file_path} tidak ditemukan dalam direktori.")