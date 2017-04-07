#!/usr/bin/env python
import paramiko


def run(choice_data, choice_cmd):
    data = choice_data[0]
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=data['ip'], port=data['port'], username=data['host_user'], password=data['host_passwd'])

    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(choice_cmd)
    # 获取命令结果
    result = stdout.read()

    # 关闭连接
    ssh.close()
    print(data['ip'].center(50, '-') + '\n', result.decode())