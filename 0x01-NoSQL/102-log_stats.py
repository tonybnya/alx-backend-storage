#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of the most present IPs
in the collection nginx of the database logs:

- The IPs top must be sorted (like the example below)
"""


if __name__ == "__main__":
    """ Improve 12-log_stats.py """
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    print(f"{collection.estimated_document_count()} logs")
    print("Methods:")

    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    status_get = collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print(f"{status_get} status check")

    print("IPs:")

    topIps = collection.aggregate([
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])

    for top_ip in top_ips:
        print(f"\t{top_ip.get('ip')}: {top_ip.get('count')}")
