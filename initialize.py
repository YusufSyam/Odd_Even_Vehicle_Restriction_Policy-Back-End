from app.utils.const.directory import get_folder_list
import os

for directory_path in get_folder_list():
  if not os.path.exists(directory_path):
      os.makedirs(directory_path)
      print(f"Direktori '{directory_path}' telah dibuat.")
  else:
      print(f"Direktori '{directory_path}' sudah ada.")