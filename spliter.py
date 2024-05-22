from Server import find_unit_line_number
import time


if __name__ == "__main__":
    # file_path = 'E:/Server/5nm/CoCrNiTension.xyz'
    file_path = "D:\Atomsk\Model\合金拉伸\CoNiCr\剪切\shear.xyz"
    unit_header = "ITEM: TIMESTEP"

    line_number = find_unit_line_number(file_path, unit_header)

    idx = 1
    start_line = 1
    end_line = start_line + line_number
    unit_data = []

    start_time = time.time()
    with open(file_path, 'r', encoding='utf-8') as file:
        for current_line, line in enumerate(file, start=1):
            if current_line >= start_line:
                unit_data.append(line)
            if current_line == end_line - 1:
                start_line = current_line + 1
                end_line = start_line + line_number
                unit_data = ''.join(unit_data)
                unit_file_name = f"D:\Atomsk\TEMP\{idx}.xyz"
                with open(unit_file_name, 'w', encoding='utf-8') as f:
                    f.write(unit_data)
                idx += 1
                unit_data = []

    end_time = time.time()
    print(f"Cost time: {end_time - start_time}")