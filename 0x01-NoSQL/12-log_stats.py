#!/usr/bin/env python3
"""
Python script that provides some stats about Nginx logs stored in MongoDB:
- Database: logs
- Collection: nginx
- Display (same as the example):
    - first line: `x` `logs` where `x` is the number of documents in this'
    collection.
    - second line: `Methods:`
    - 5 lines with the number of documents with the
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    in this order (see example below).
    - one line with the number of documents with:
        - method=GET
        - path=/status

EXAMPLE:
--------
>> ./12-log_stats.py
94778 logs
Methods:
    method GET: 93842
    method POST: 229
    method PUT: 0
    method PATCH: 0
    method DELETE: 0
47415 status check
"""
from pymongo import MongoClient


def nginx_logs_stats():
    """
    Gets the stats from Nginx logs stored in MongoDB
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    logs = collection.find()
    # Number of methods found in logs
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_count = {
        "GET": 0, "POST": 0, "PUT": 0, "PATCH": 0, "DELETE": 0
    }
    # Number of documents with GET method and path=/status
    status_check = 0

    for log in logs:
        method = log.get("method", "")
        path = log.get("path", "")

        if method in methods:
            method_count[method] += 1

        if method == 'GET' and path == "/status":
            status_check += 1

    print("{} logs".format(collection.count_documents({})))
    print("Methods:")
    for method in methods:
        print("\tmethod {}: {}".format(method, method_count[method]))
    print("{} status check".format(status_check))


if __name__ == "__main__":
    nginx_logs_stats()
