from Server import find_unit_line_number
import time


if __name__ == "__main__":
    # file_path = 'E:/Server/5nm/CoCrNiTension.xyz'
    file_path = "F:/CoCrNi/erate=2.5e-8/5nm"
    unit_header = "ITEM: TIMESTEP"

    splite_num = 16
    tot_num = 100

    _div, _mod = divmod(tot_num, splite_num)

    line_number = find_unit_line_number(file_path, unit_header)

    idx = 1
    start_line = 1
    end_line = start_line + line_number * _div
    unit_data = []

    start_time = time.time()
    with open(file_path, 'r', encoding='utf-8') as file:
        for current_line, line in enumerate(file, start=1):
            if current_line >= start_line:
                unit_data.append(line)
            if current_line == end_line - 1:
                if idx == splite_num:
                    start_line = current_line + 1
                    end_line = start_line + line_number * _mod
                else:
                    start_line = current_line + 1
                    end_line = start_line + line_number * _div
                unit_data = ''.join(unit_data)
                unit_file_name = f"D:/Atomsk/TEMP/{idx}.xyz"
                with open(unit_file_name, 'w', encoding='utf-8') as f:
                    f.write(unit_data)
                idx += 1
                unit_data = []


    end_time = time.time()
    print(f"Cost time: {end_time - start_time}")