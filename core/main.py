#!/usr/bin/env python
from concurrent.futures import ThreadPoolExecutor
from core import db_handler
from core import conn_ssh
from core import rpc_conn

state = None


def login(user, passwd):
    sql = db_handler.db_handler()
    data = sql('select', 'select * from user_msg')
    for d in data:
        if d['username'] == user and d['password'] == passwd:
            return d['id']
    else:
        return False


def user_host(user_id):
    sql = db_handler.db_handler()
    data = sql(
        'select',
        'select * from user_host_relational \
        left join host on user_host_relational.host_id = host.id \
        where user_id=%d' % user_id
    )
    return data


def insert_host_sql(ip, port, host_user, host_passwd, user_id):
    sql = db_handler.db_handler()
    new_id = sql(
        'insert',
        "insert into host(ip,port,host_user,host_passwd) values(%s,%s,%s,%s)",
        data=(ip, port, host_user, host_passwd)
    )
    if new_id[0]:
        sql(
            'insert',
            'insert into user_host_relational(user_id,host_id) values(%s,%s)',
            data=(user_id, new_id[0])
        )
    else:
        return 'Failed to add the host address'
    return 'Add the host success'


def delete_host_sql(ip, user_id):
    sql = db_handler.db_handler()
    effect_row = sql(
        'delete',
        'delete from user_host_relational \
        where host_id = (select id from host where ip=%s) and user_id=%s',
        data=(ip, user_id)
    )
    if effect_row[1]:
        effect_row2 = sql(
            'delete',
            'delete from host where ip=%s',
            data=(ip)
        )
    else:
        return 'Failed to delete the host address'
    return effect_row[1], effect_row2[1]


def update_host_sql(ip, column, value):
    sql = db_handler.db_handler()
    effect_row = sql(
        'update',
        'update host set %s' % column + '=%s where ip=%s',
        data=(value, ip)
    )
    if effect_row[1] is None:
        return 'Failed to update the host address'
    return effect_row[1]


def thread_pool(choice_ip, choice_cmd, choice_data):
    pool = ThreadPoolExecutor(2)
    for ip in choice_ip:
        print('start ... ssh %s' % ip)
        # 去连接池中获取链接
        # future中包含命令结果
        pool.submit(rpc_conn.run, ip, choice_cmd)
    # 等待线程执行完成
    pool.shutdown()


def host_shell(dic_data):
    host_data = cat_host()
    choice_ip = input('Please enter the management host address: ').split(',')
    choice_cmd = input('Please enter a command to execute: ')
    choice_data = list(filter(lambda x: x['ip'] in choice_ip, host_data))
    thread_pool(choice_ip, choice_cmd, choice_data)
    # print(choice_ip.center(50, '-') + '\n', conn_ssh.run(choice_data, choice_cmd).decode())


def cat_host():
    host_data = user_host(state)
    if len(host_data) > 0:
        for ip in host_data:
            print(ip['ip'])
    else:
        print('No hosts available')
    return host_data


def insert_host(dic_data):
    ip = input('ip:')
    port = int(input('port:'))
    host_user = input('host_user:')
    host_passwd = input('host_passwd:')
    code = insert_host_sql(ip, port, host_user, host_passwd, dic_data['state'])
    print(code)


def delete_host(dic_data):
    cat_host()
    ip = input('delete ip:')
    code = delete_host_sql(ip, dic_data['state'])
    print(code)


def update_host(dic_data):
    cat_host()
    ip = input('update ip:')
    column = input('The input change column:')
    value = input('The input change value:')
    code = update_host_sql(ip, column, value)
    print(code)

def logout(dic_data):
    exit('Successfully logged off')


def interactive(dic_data):
    '''
    interact with user
    '''
    menu = u'''
    -------  Bank ---------
    \033[32;1m1.  执行shell命令
    2.  查看服务器地址
    3.  增加服务器地址
    4.  修改服务器地址
    5.  删除服务器地址
    6.  退出
    \033[0m'''
    menu_dic = {
        '1': host_shell,
        '2': cat_host,
        '3': insert_host,
        '4': update_host,
        '5': delete_host,
        '6': logout,
    }
    # exit_flag = False
    while True:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            if user_option == '2':
                menu_dic[user_option]()
            else:
                menu_dic[user_option](dic_data)
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def run():
    global state
    print('HOST MANAGE SYSTEM'.center(50, '*'))
    num = 0
    while num < 3:
        _user = input('username: ')
        _passwd = input('password: ')
        state = login(_user, _passwd)
        if state:
            break
        else:
            print('The user name or password error')
            num += 1
    else:
        exit('The user to try more than three times')
    host_data = user_host(state)
    dic_data = {
        '_user': _user,
        'state': state,
        'host_data': host_data
    }
    interactive(dic_data)
