from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=["192.168.6.153:9092"])
msg = './static/images/img336.jpg'.encode('utf-8')
producer.send('test', msg)
producer.close()




