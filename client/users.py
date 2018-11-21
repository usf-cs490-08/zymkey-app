import re
from threading import Thread
from confluent_kafka import Consumer, Producer, OFFSET_BEGINNING

class UserStatusManager(Thread):

    USER_TOPIC = 'USER_STATUS'
    STATUS_DELIM = '$$'

    def __init__(self, brokers, user, userStatusMap):
        super(UserStatusManager, self).__init__()
        self.user = user
        self.producer = UserStatusManager.createProducer(brokers)
        self.consumer = UserStatusManager.createConsumer(brokers, user)
        self.userStatusMap = userStatusMap
        self.shutdownNow = False
        self.start()

    @staticmethod
    def createProducer(brokers):
        config = {'bootstrap.servers': brokers}
        return Producer(**config) 

    @staticmethod
    def createConsumer(brokers, user):
        conf = {'bootstrap.servers': brokers, 'group.id': user + '-group', 'auto.offset.reset': 'earliest'}
        return Consumer(conf)

    def goOnline(self):
        self.__sendStatus(True)

    def goOffline(self):
        self.__sendStatus(False)
        self.shutdownNow = True

    def __sendStatus(self, isOnline):
        s = 'online' if isOnline else 'offline'
        message = '%s%s%s' % (self.user, self.STATUS_DELIM, s) 
        try:
            self.producer.produce(self.USER_TOPIC, message)
            self.producer.poll(10) # wait for callback
            self.producer.flush()
        except BufferError:
            print('error : producer queue is full (%d messages awaiting delivery): \n' % len(p))

    def subscribe(self):

        def reset(consumer, partitions):
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            self.consumer.assign(partitions)

        self.consumer.subscribe([self.USER_TOPIC], on_assign=reset)

    def run(self):

        self.subscribe()

        while not self.shutdownNow:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                pass
            else:
                timestamp = msg.timestamp()[1]
                userStatus = re.split('\$\$', msg.value().decode('utf-8'))

                if len(userStatus) == 2:
                    user = userStatus[0]
                    isOnline = userStatus[1]
                    self.userStatusMap.putStatus(user, isOnline, timestamp)

        self.consumer.close()        

