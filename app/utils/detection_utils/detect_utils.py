import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import datetime
import re


def limit_at_zero(x):
    return x if x>=0 else 0

def display_images_in_subplot(df, num_cols=3, cols_to_plot='car_img_filename', cols_for_title= 'raw_license_plate_text'):
    num_rows = (len(df) + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

    for i, row in df.iterrows():
        img_path = row[cols_to_plot]

        try:
          img = mpimg.imread(img_path)
        except:
          print(f'No Image From Column {cols_to_plot} for Index {i}')
          continue
          
        # title = f"car_id: {row['car_id']}, plate: {row[cols_for_title]}"
        title = f"Plat Nomor: {row[cols_for_title]}"

        if num_rows > 1:
            ax = axes[i // num_cols, i % num_cols]
        else:
            ax = axes[i % num_cols]

        ax.imshow(img, cmap='gray')
        ax.set_title(title)
        ax.axis('off')

    if len(df) < num_rows * num_cols:
        for i in range(len(df), num_rows * num_cols):
            fig.delaxes(axes.flatten()[i])

    plt.tight_layout()
    plt.show()

def get_car(license_plate, vehicle_track_ids):
    x1, y1, x2, y2, score, class_id = license_plate

    if len(vehicle_track_ids)<=0:
        return -1, -1, -1, -1, -1

    foundIt = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]
        print(xcar1, ycar1, xcar2, ycar2)
        if x1 >= xcar1 and y1 >= ycar1 and x2 <= xcar2 and y2 <= ycar2:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return vehicle_track_ids[car_indx]

    return -1, -1, -1, -1, -1

import re

def get_license_plate_num(input_string):
    digits_combined = ''.join(re.findall(r'\d', input_string))

    return digits_combined

def get_is_car_violating(license_plate_num):
    if (license_plate_num%2==0 and TODAYS_POLICY=="genap") or (license_plate_num%2==1 and TODAYS_POLICY=="ganjil"):
        return 0
    else:
        return 1

import shutil

def clean_path(path_list):
    for folder_path in path_list:
        if os.path.exists(folder_path):
            # Loop melalui semua file dalam direktori dan hapus satu per satu
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        # Opsional: Jika ingin menghapus direktori beserta isinya, gunakan os.rmdir()
                        # os.rmdir(file_path)
                        pass
                except Exception as e:
                    print(f"Error: {e}")

            print(f"Semua file dalam '{folder_path}' telah dihapus.")
        else:
            print(f"Direktori '{folder_path}' tidak ditemukan.")

def calculate_frame_skip(original_fps, target_fps):
    frame_skip = round(original_fps / target_fps)

    return frame_skip


def check_todays_policy():
    today_date = datetime.date.today().day

    if today_date % 2 == 0:
        return "genap"
    else:
        return "ganjil"

def get_is_car_violating(license_plate_num):
    todays_policy= check_todays_policy()
    if (license_plate_num%2==0 and todays_policy=="genap") or (license_plate_num%2==1 and todays_policy=="ganjil"):
        return 0
    else:
        return 1
        
def get_license_plate_num(input_string):
    digits_combined = ''.join(re.findall(r'\d', input_string))

    return int(digits_combined)

def get_plate_type(license_plate_num):
    return "genap" if license_plate_num%2==0 else "ganjil"