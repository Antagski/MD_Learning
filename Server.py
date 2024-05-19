import os
import sys


def find_unit_line_number(file_path, unit_header):
    with open(file_path, 'r', encoding='utf-8') as file:
        line_count = 0
        header_count = 0
        for line in file:
            line_count += 1
            if unit_header in line:
                header_count += 1
                if header_count == 2:
                    line_count -= 1
                    break

    return line_count


def read_unit(file_path, unit_number, line_number, unit_header):
    start_line = (unit_number - 1) * line_number + 1
    end_line = start_line + line_number
    unit_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for current_line, line in enumerate(file, start=1):
            if current_line >= start_line:
                unit_data.append(line)
            if current_line == end_line - 1:
                break

    return ''.join(unit_data)


# Example usage
if __name__ == "__main__":
    file_path = '/root/autodl-tmp/CoCrNi/Tension/5nm/CoCrNiTension.xyz'

    unit_header = "ITEM: TIMESTEP"

    # 求解单元长度
    line_number = find_unit_line_number(file_path, unit_header)

    # 读取特定单元数据
    unit_number = int(sys.argv[1])
    unit_data = read_unit(file_path, unit_number, line_number, unit_header)

    print(unit_data)
