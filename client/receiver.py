import re
from threading import Thread
from confluent_kafka import Consumer, TopicPartition, OFFSET_BEGINNING

class MessageReceiver(Thread):

    def __init__(self, brokers, user, history):
        super(MessageReceiver, self).__init__()
        self.user = user
        self.history = history
        self.offsetMap = {}
        self.consumer = MessageReceiver.createConsumer(brokers, user)
        self.shutdownNow = False
        self.start()

    @staticmethod
    def createConsumer(brokers, user):
        conf = {'bootstrap.servers': brokers, 'group.id': user + '-group',
                'auto.offset.reset': 'earliest', 'session.timeout.ms': 6000, 'enable.auto.commit': False, 'metadata.max.age.ms': 500}
        return Consumer(conf)

    def shutdown(self):
        self.shutdownNow = True

    def subscribe(self):

        # TODO instead of trying to get/change offets here, just save partitions
        def storeOffsetsAndReset(consumer, partitions):
            for p in partitions:
                self.offsetMap['%s$%d' % (p.topic, p.partition)] = p.offset
                p.offset = OFFSET_BEGINNING
            self.consumer.assign(partitions)

        self.consumer.subscribe(['GLOBAL', '^.*\\b' + self.user + '\\b.*'], on_assign=storeOffsetsAndReset)

    def isUnread(self, msg):
        last = self.offsetMap['%s$%d' % (msg.topic(), msg.partition())]
        print('%s$%d  - last : %d  - cur : %d' % (msg.topic(), msg.partition(), last, msg.offset()))
        return msg.offset() > last

    def run(self):

        self.subscribe()

        # TODO after saving partitions, get/change offets here using seek()

        while not self.shutdownNow:
            msg = self.consumer.poll()
            if msg is None:
                continue
            if msg.error():
                print(msg.error())
                pass
            else:
                users = re.split('-', msg.topic())
                val = msg.value().decode('utf-8')
                timestamp = msg.timestamp()[1]
                self.history.putMessage(users, val, timestamp)

                if self.isUnread(msg):
                    print('new message!', flush=True)

                self.consumer.commit(msg)

        self.consumer.close()        

