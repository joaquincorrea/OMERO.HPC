#! /usr/bin/env python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Written (W) 2012-2013 Seung-Jin Sul (ssul@lbl.gov)
# Copyright (C) NERSC, LBL


#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------

VERSION = "2.4"
RMQ_HOST = ''
RMQ_USER = ''
RMQ_PASS = ''
RMQ_VHOST = ''
RMQ_PORT = ''

MAIN_EXCH = "_MAIN_EXCHANGE"
TASKQ_POSTFIX = "_TASK_QUEUE"           ## taskqueuenqme = userid+taskqueuename+TASKQ_POSTFIX
RESUQ_POSTFIX = "_RESULT_QUEUE"         ## resultqueueanme = serid+taskfilename+RESUQ_POSTFIX
CLIENT_HB_EXCH = '_CLIENT_HB_EXCHANGE'  ## client exchange name = userid+taskqueuename+CLIENT_HB_EXCH
WORKER_HB_EXCH = '_WORKER_HB_EXCHANGE'  ## worker exchange name = userid+taskqueuename+WORKER_HB_EXCH
WORKER_HB_POSTFIX = '_WORKER_HB_QUEUE'  ## worker hb queue name = userid+taskqueuename+WORKER_HB_POSTFIX
CLIENT_HB_POSTFIX = '_CLIENT_HB_QUEUE'  ## client hb queue name = userid+taskqueuename+CLIENTR_HB_POSTFIX

CLIENT_HB_RECEIVE_INITIAL_INTERVAL = 1  ## client's heartbeat receiving interval in sec
CLIENT_HB_RECEIVE_INT_INC_MUL = 3.0     ## client's heartbeat increase multiplier
CLIENT_HB_RECEIVE_INT_INC_RATE = 1.2    ## client's heartbeat increase rate

CLIENT_HB_SEND_INTERVAL = 5             ## client's heartbeat sending interval in sec (client->worker)
WORKER_HB_RECEIVE_INTERVAL = 10         ## worker's heartbeat receiving interval in sec
WORKER_HB_SEND_INTERVAL = 5             ## worker's heartbeat sending interval in sec (worker->client)
WORKER_TIMEOUT = 30                     ## worker's timeout for waiting the client's hearbeat
OOM_WARNING_THRESH = 90                 ## out-of-mem warning threshold

FILE_CHECKING_MAX_TRIAL = 3             ## max number of trial for checking
FILE_CHECK_INTERVAL = 3                 ## sleep time between output file checking before retiral
FILE_CHECK_INT_INC = 1.5                ## increase amount of wait time for file checking

CLIENT_FILE_LOGGING = True              ## enable/disable file logging
WORKER_FILE_LOGGING = True



## EOF
