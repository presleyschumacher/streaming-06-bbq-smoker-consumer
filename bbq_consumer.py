"""
    This program listens for work messages contiously. 
    
    The bbq_producer.py must run to start sending the messge first
    We want know if (Condition To monitor):
        The smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert!)
        Any food temperature changes less than 1 degree F in 10 minutes (food stall!)
### Name:  Presley Schumacher
### Date:  February 21, 2023
"""
import pika
import sys
import time
from collections import deque





