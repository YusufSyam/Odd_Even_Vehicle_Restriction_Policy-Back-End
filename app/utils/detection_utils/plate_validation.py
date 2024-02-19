import re

# Dictionary yang diberikan
dict_char_to_int = {
                    'A': '4',
                    'B': '8',
                    'C': '0',
                    'D': '0',
                    'E': '3',
                    'F': '7',
                    'G': '6',
                    'H': '4',
                    'I': '1',
                    'J': '3',
                    'K': '4',
                    'L': '4',
                    # 'L': '1',
                    'M': '7',
                    'N': '7',
                    'O': '0',
                    'P': '9',
                    'Q': '0',
                    'R': '7',
                    'S': '5',
                    'T': '7',
                    'U': '0',
                    'V': '7',
                    'W': '7',
                    'X': '4',
                    'Y': '4',
                    'Z': '2'
                    }

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '2':'Z',
                    '3': 'J',
                    '4': 'A',
                    '5': 'S',
                    '6': 'G',
                    '7':'T',
                    '8':'B',
                    '9': 'P'}

start_plate_char_dict={
    'sulsel':'DD'
}

def ganti_karakter(input_string, char_to_int_dict):
    hasil = ''.join(char_to_int_dict.get(char, char) for char in input_string)
    return hasil

def ganti_karakter_awal(input_string, loc=None):
    global start_plate_char_dict
    if loc is None or loc not in start_plate_char_dict.keys():
      return input_string
    
    return start_plate_char_dict[loc]

def ambil_huruf_terbatas(input_string, min= 1, max= 3):
    pattern = re.compile(f'[a-zA-Z]{{{min},{max}}}')
    hasil = re.search(pattern, input_string)
    if hasil:
        return hasil.group(0)
    else:
        return ''


def filter_huruf_dan_angka(input_string):
    pattern = re.compile(r'[a-zA-Z0-9 ]+')
    hasil = re.findall(pattern, input_string)
    return ''.join(hasil)

# Kalau jelek ocr nya
def pisah_string(input_string, max_pattern=4):
    pattern_n_huruf_angka = re.compile(f'([a-zA-Z0-9]{{{max_pattern}}})')
    match_n_huruf_angka = re.search(pattern_n_huruf_angka, input_string)

    if match_n_huruf_angka:
        posisi_awal_n_huruf_angka = match_n_huruf_angka.start()
        posisi_akhir_n_huruf_angka = match_n_huruf_angka.end()

        bagian_n_huruf_angka = match_n_huruf_angka.group(1)
        bagian_sebelumnya = input_string[:posisi_awal_n_huruf_angka].strip()
        bagian_setelahnya = input_string[posisi_akhir_n_huruf_angka:].strip()

        return bagian_sebelumnya, bagian_n_huruf_angka, bagian_setelahnya

    # Coba lagi tapi diikurangi max pattern nya
    elif max_pattern>=2:
        return pisah_string(input_string, max_pattern-1)
    else:
        return None


def validate_raw_plate_text(text, loc='sulsel'):
  # print('=======================================\n')
  # print(text)

  test_plate= text.upper()
  test_plate_split= pisah_string(test_plate)

  if test_plate_split is None:
    print(f'{test_plate} is not validated')
    return test_plate

  # print(test_plate_split)
  # test_plate_split= map(filter_huruf_dan_angka, test_plate_split)
  # print(test_plate_split)

  start, mid, end= test_plate_split

  # print(start, mid, end)

  start= ganti_karakter(start, dict_int_to_char)
  mid= ganti_karakter(mid, dict_char_to_int)
  end= ganti_karakter(end, dict_int_to_char)

  # print(start, mid, end)

  start= ambil_huruf_terbatas(start)
  if loc is not None:
    start= ganti_karakter_awal(start, loc)

  end= ambil_huruf_terbatas(end)

  start, mid, end= map(filter_huruf_dan_angka, [start, mid, end])

  # print(start, mid, end)

#   validated= (''.join([i for i in [start, mid, end]])).strip()
  validated= (' '.join([i for i in [start, mid, end]])).strip()

  # print(f'{validated}\n=======================================')

  return validated
