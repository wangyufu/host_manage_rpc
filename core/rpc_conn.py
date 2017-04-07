#!/usr/bin/env python
import threading
import uuid
import pika
import json

import time
from conf import settings


def run(ip, choice_cmd):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RabbitMQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange='rpc', type='direct')

    corr_id = str(uuid.uuid4())
    channel.queue_declare(queue=corr_id, durable=True)
    message_obj = json.dumps({'corr_id': corr_id, 'choice_cmd': choice_cmd}).encode(encoding='utf-8')
    print(ip)
    channel.basic_publish(exchange='rpc', routing_key=ip, body=message_obj)

    def callback(ch, method, properties, body):
        print(ip.center(50, '-') + '\n', body.decode())
        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.stop_consuming()
        ch.queue_delete(corr_id)

    # channel.basic_consume(callback, queue=corr_id, no_ack=True)
    # # channel.consume(corr_id, no_ack=True,  # pylint: disable=R0913
    # #                 inactivity_timeout=5.0)
    # channel.start_consuming()
    # 等待客户端想队列中发送执行结果，超时时间10s
    v = channel.consume(corr_id, inactivity_timeout=10)
    try:
        for method, properties, body in v:
            # 执行指定回调函数
            callback(channel, method, properties, body)
    except TypeError as e:
        # 如果超时，则删除临时队列，不再获取数据
        channel.queue_delete(corr_id)

    connection.close()