#! /usr/bin/env python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Written (W) 2012-2013 Seung-Jin Sul (ssul@lbl.gov)
# Copyright (C) NERSC, LBL

from Config import *
from Common import *

"""
Created on Apr 11 2013

RabbitMQ connection and communication wrapper class.

@author Seung-Jin
"""
class RmqConnection(object):
    __connection = None
    
    def __init__(self): # return a pika connection
        if not self.__connection:
            creds = pika.PlainCredentials(RMQ_USER, RMQ_PASS)
            params = pika.ConnectionParameters(credentials=creds,
                                               host=RMQ_HOST,
                                               virtual_host=RMQ_VHOST)
            self.__connection = pika.BlockingConnection(params)
        else:
            print "Already connected."
                    
    def open(self):
        return self.__connection

    def close(self):
        self.__connection.close()
        

"""
Created on Apr 6 2013

RabbitMQ connection and communication wrapper class.
Note that "consume" takes callback function.

@author Seung-Jin
"""

## To do
## - logger
## - multiprocessing
class RmqConnection2(object):
    
    __conn = None
    __chan = None
    __exchType = None     ## exchagen tyep: fanout, direct, topic, header
    __exchangeName = None ## exchange name
    
    def __init__(self, exchange_name, exchange_type="direct"):
        self.__creds = pika.PlainCredentials(RMQ_USER, RMQ_PASS)
        self.__params = pika.ConnectionParameters(credentials=self.__creds,
                                                  host=RMQ_HOST,
                                                  virtual_host=RMQ_VHOST)
        self.__exchangeName = exchange_name
        self.__exchType = exchange_type
        self.__rmqOpenConn()
        
    def __rmqOpenConn(self):
        self.__conn = pika.BlockingConnection(self.__params)
        
    def __rmqOpenChannel(self, confirm=True):
        self.__chan = self.__conn.channel()
        if confirm:
            self.__chan.confirm_delivery()
            
    def __rmqDeclareExchange(self, durable=False, auto_delete=True):
        self.__chan.exchange_declare(exchange=self.__exchangeName,
                                     type=self.__exchType,
                                     #durable=False, auto_delete=False)
                                     durable=durable, auto_delete=auto_delete)
    
    def __rmqDeclareQueue(self, queue, durable=False, exclusive=True, auto_delete=True):
        self.__chan.queue_declare(queue=queue,
                                  #durable=False, exclusive=False, auto_delete=False)
                                  durable=durable,
                                  exclusive=exclusive,
                                  auto_delete=auto_delete)
    
    def __rmqQueueBind(self, queue, exchange, routing_key=""):
        self.__chan.queue_bind(queue=queue,
                               exchange=exchange,
                               routing_key=routing_key)    
    
    def publish(self, msg, routing_key, delivery_mode=2, mandatory=True):
        ## These calls are mandatory for detecting disconnection and waiting for
        ## reconection.
        self.__rmqOpenConn()
        self.__rmqOpenChannel()
        self.__rmqDeclareExchange()

        if not self.__chan.basic_publish(exchange=self.__exchangeName,
                                         routing_key=routing_key,
                                         body=msg,
                                         properties=pika.BasicProperties(
                                               content_type = "text/plain",
                                               delivery_mode = delivery_mode, # persistent
                                               ),
                                         mandatory=mandatory
                                         ):   
            if mandatory:
                print 'Message was returned. No queue found.'
            else:
                print 'Message was not confirmed'
                
    def publishAndWait(self):
        pass
    
    def consume(self, queue, routing_key, callback, basic_qos=0):
        ## These calls are mandatory for detecting disconnection and waiting for
        ## reconection.
        self.__rmqOpenConn()
        self.__rmqOpenChannel()
        self.__rmqDeclareExchange()
        self.__rmqDeclareQueue(queue)
        
        print "Binding queue %s to exchange %s" % (queue, self.__exchangeName)
        self.__rmqQueueBind(queue, self.__exchangeName, routing_key)

        print "Listening to queue %s" % (queue)
        if basic_qos > 0:
            self.__chann.basic_qos(prefetch_count=basic_qos)
        self.__chan.basic_consume(callback, queue=queue)
        self.__chan.start_consuming()
        
        print 'Connection closed. Reason:', self.__conn.connection_close
        
    """
    @return (method, header, body)
    """
    def consumeOne(self, queue, routing_key, no_ack=True):
        ## These calls are mandatory for detecting disconnection and waiting for
        ## reconection.
        self.__rmqOpenConn()
        self.__rmqOpenChannel()
        self.__rmqDeclareExchange()
        self.__rmqDeclareQueue(queue)
        self.__rmqQueueBind(queue, self.__exchangeName, routing_key)
        
        return self.__chan.basic_get(queue=queue, no_ack=no_ack)
            
## EOF
