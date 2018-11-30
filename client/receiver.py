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
                'auto.offset.reset': 'earliest', 'enable.auto.commit': True, 
                'session.timeout.ms': 6000, 'metadata.max.age.ms': 500, 
                'topic.metadata.refresh.interval.ms': 1000}
        return Consumer(conf)

    def shutdown(self):
        self.shutdownNow = True

    def subscribe(self):
        def storeOffsetsAndReset(consumer, partitions):
            for p in self.consumer.committed(partitions):
                self.offsetMap['%s$%d' % (p.topic, p.partition)] = p.offset
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            self.consumer.assign(partitions)

        self.consumer.subscribe(['GLOBAL', '^.*\\b' + self.user + '\\b.*'], on_assign=storeOffsetsAndReset)

    def isUnread(self, msg):
        next = self.offsetMap['%s$%d' % (msg.topic(), msg.partition())]
        return msg.offset() >= next

    def run(self):

        self.subscribe()

        while not self.shutdownNow:
            msg = self.consumer.poll()
            if msg is None or msg.error():
                pass
            else:
                users = re.split('-', msg.topic())
                val = msg.value().decode('utf-8')

                # JSON parsing
                '''
                json = val.split(',')
                user = re.sub('[^a-zA-Z0-9]', '', json[0].split(':')[1])
                content = re.sub('[^a-zA-Z0-9]', '', json[1].splitz(':')[1])
                '''
                timestamp = msg.timestamp()[1]
                self.history.putMessage(users, val, timestamp)

                if self.isUnread(msg):
                    print('new message!', flush=True)
                    # From field parsed from the JSON object
                    #print('new message from {}!'.format(user), flush=True)

                self.consumer.commit(msg)

        self.consumer.close()        

