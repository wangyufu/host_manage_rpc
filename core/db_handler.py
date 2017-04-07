#!/usr/bin/env python
import pymysql
from conf import settings

def db_handler():
    '''
    connect to db
    :param conn_parms: the db connection params set in settings
    :return:a
    '''
    conn_params = settings.DATABASE_TYPE
    if conn_params == 'file_storage':
        pass
    elif conn_params == 'mysql':
        return mysql_execute


def db_conn():
    db_set = settings.DATABASE_CONN
    conn = pymysql.connect(
        host=db_set['host'], port=db_set['port'], user=db_set['user'], passwd=db_set['passwd'], db=db_set['db']
    )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn, cursor


def mysql_execute(action, sql, **kwargs):
    if action == 'select':
        conn, cursor = db_conn()
        cursor.execute(sql)
        # 获取第一行数据
        # row_1 = cursor.fetchone()
        # 获取前n行数据
        # row_2 = cursor.fetchmany(3)
        # 获取所有数据
        row_3 = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return row_3
    elif action == 'insert' or action == 'delete' or action == 'update':
        conn, cursor = db_conn()
        # 执行SQL，并返回收影响行数
        effect_row = cursor.execute(sql, kwargs['data'])
        conn.commit()
        cursor.close()
        conn.close()
        # 获取最新自增ID
        new_id = cursor.lastrowid
        return new_id, effect_row

