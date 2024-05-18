import paramiko

host = "connect.bjb1.seetacloud.com"
port = 15616
username = "root"
password = "ZyLl4Fzi4NUf"

def test_ssh_connection():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
        print("SSH connection successful.")
        ssh.close()
    except Exception as e:
        print(f"SSH connection failed: {e}")

if __name__ == "__main__":
    test_ssh_connection()
