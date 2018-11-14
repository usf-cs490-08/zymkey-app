# Low Level Design

This document specifies the message format and workflow of a transaction. In this scenario, a transaction is defined to be a process in which a message is sent from client A to client B. The message is sent to a Kafka topic as a JSON object.

## Basic message format:
```
{
    "to" : Bob
    "from" : Alice
    "message" : "encrypted message with a shared key"
}
```

## Message format that supports verification
```
{
    "to" : Bob
    "from" : Alice
    "message" : "encrypted message with a shared key"
    "signature" : "signed value of the encrypted message"
}
```
