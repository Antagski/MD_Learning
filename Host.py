import paramiko
import os
import subprocess
from render import render_image, render_anim, read_file


def get_remote_unit_data(host, port, username, password, unit_number):
    command = f"python3 /root/autodl-tmp/py/Server.py {unit_number}"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    stdin, stdout, stderr = ssh.exec_command(command)
    unit_data = stdout.read().decode('utf-8')

    ssh.close()
    return unit_data


def save_to_temp_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)


def visualize_data(temp_file, output_image):
    vp = read_file(PATH=temp_file)
    render_image(vp, filename=output_image)


def main():
    host = "connect.bjb1.seetacloud.com"
    port = 15616
    username = "root"
    password = "ZyLl4Fzi4NUf"

    temp_file = "TEMP.xyz"
    output_image = "image.png"

    while True:
        unit_number = int(input("Enter the unit number to retrieve: "))
        if unit_number == -1:
            return

        # 获取远程单元数据
        unit_data = get_remote_unit_data(host, port, username, password, unit_number)

        # 保存到本地缓存文件
        save_to_temp_file(unit_data, temp_file)

        # 可视化数据
        visualize_data(temp_file, output_image)

        # 显示图片（例如，使用PIL）
        from PIL import Image
        img = Image.open(output_image)
        img.show()

        # 清理文件
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(output_image):
            os.remove(output_image)


if __name__ == "__main__":
    main()
