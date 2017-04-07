#!/usr/bin/env python
import json
import pika
import subprocess
# RabbitMQ server address
RabbitMQ = '192.168.1.122'
# 本机地址
agent = '192.168.1.122'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RabbitMQ))
channel = connection.channel()

channel.exchange_declare(exchange='rpc', type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='rpc', queue=queue_name, routing_key=agent)


def callback(ch, method, properties, body):
    body_obj = json.loads(body.decode(encoding='utf-8'))
    print("%s" % body_obj['choice_cmd'])
    res = subprocess.Popen(body_obj['choice_cmd'],
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    err = res.stderr.read()
    if err:
        back_msg = err
    else:
        back_msg = res.stdout.read()
    channel.basic_publish(exchange='',
                          routing_key=body_obj['corr_id'],
                          body=back_msg,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))


channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()