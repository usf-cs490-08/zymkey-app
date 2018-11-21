from confluent_kafka import Producer

class MessageSender:

    def __init__(self, brokers, user):
        self.producer = MessageSender.createProducer(brokers) 
        self.user = user

    @staticmethod
    def createProducer(brokers):
        config = {'bootstrap.servers': brokers}
        return Producer(**config) 

    def sendMessage(self, userList, message):
        userList.sort()
        topic = '-'.join(userList)

        def delivery_callback(err, msg):
            if err:
                print('sending error: %s' % err)
            else:
                print('message sent!')
        try:
            self.producer.produce(topic, message, on_delivery=delivery_callback)
            self.producer.poll(5) # wait for callback
            self.producer.flush()
        except BufferError:
            print('error : producer queue is full (%d messages awaiting delivery): \n' % len(p))
