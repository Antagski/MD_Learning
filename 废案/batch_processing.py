import subprocess


def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        print("Command output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")


if __name__ == "__main__":
    # 文件列表
    files = ['cubic_1nm', 'cubic_3nm', 'cubic_5nm', 'cubic_7nm', 'cubic_9nm', 'cubic_12nm']

    # 基础命令
    create_command_template = "atomsk --create fcc 3.48 Ni {output_file}"
    polycrystal_command_template = "atomsk --polycrystal {input_file} {element_grid_file} {output_file} -wrap"

    create_command = create_command_template.format(output_file=f"Ni.lmp")
    print(f"Running command: {create_command}")
    run_command(create_command)

    for file in files:
        element_grid_file = f"{file}.txt"
        output_file = f"Poly_{file}.lmp"

        # 创建命令
        polycrystal_command = polycrystal_command_template.format(
            input_file=f"Ni.lmp",
            element_grid_file=element_grid_file,
            output_file=output_file
        )

        print(f"Running command: {polycrystal_command}")
        run_command(polycrystal_command)
