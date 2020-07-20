from kafka import KafkaConsumer
consumer = KafkaConsumer('test',bootstrap_servers=["192.168.6.153:9092"] )
recv1 = ''
for msg in consumer:
    # str(msg, encoding="utf-8")
    # recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, bytes.decode(msg.value))
    recv = "%s:%d:%d: value=%s" % (msg.topic, msg.partition, msg.offset,  bytes.decode(msg.value))
    recv1 = recv
    print(bytes.decode(msg.value))
    print("*********************")
    print(recv)

