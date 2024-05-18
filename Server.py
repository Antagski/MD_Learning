import sys


def extract_unit(file_path, unit_number, unit_header):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    unit_data = []
    unit_count = 0
    capture = False

    for line in lines:
        if unit_header in line:
            unit_count += 1
            if unit_count == unit_number:
                capture = True
                unit_data.append(line)
            elif unit_count == unit_number + 1:
                break
        elif capture:
            unit_data.append(line)

    return ''.join(unit_data)


if __name__ == "__main__":
    file_path = '/root/autodl-tmp/CoCrNi/Shear/shear.xyz'
    unit_number = int(sys.argv[1])
    unit_header = "ITEM: TIMESTEP"  # 替换为实际的单元特征文段
    unit_data = extract_unit(file_path, unit_number, unit_header)
    print(unit_data)
