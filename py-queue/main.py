#!/usr/bin/env python

from azure.storage.queue import QueueClient
from azure.core.exceptions import ResourceExistsError
import threading
import os

infos = {
    "connectionString": os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
    "uuid": "tp1"
}

def get_queue():
    # Retrieve the connection string from an environment
    # variable named AZURE_STORAGE_CONNECTION_STRING
    connect_str = infos['connectionString']

    # Create a unique name for the queue
    q_name = "queue-" + infos["uuid"]

    print("Creating queue: " + q_name)
    queue_client = QueueClient.from_connection_string(connect_str, q_name)

    try:
        queue_client.create_queue()
    except ResourceExistsError:
        print('Already existing queue, using simple connection')

    return queue_client

def send(client: QueueClient,message = u"hello"):

    print("Adding message: " + message)
    client.send_message(message)

def receive(client: QueueClient, delete = True):
    messages = client.peek_messages()

    for peeked_message in messages:
        print("Peeked message: " + peeked_message.content)

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def main():
    c = get_queue()
    set_interval(lambda: send(c), 4)
    set_interval(lambda: receive(c), 1)

main()
