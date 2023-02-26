"""
    This program listens for work messages contiously. 
    
    The bbq_producer.py must run to start sending the messge first
    We want know if (Condition To monitor):
        The smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert!)
        
### Name:  Presley Schumacher
### Date:  February 21, 2023
"""
import pika
import sys
import time
from collections import deque

#Declare Deque
# 1 reading every 30 seconds
# 2.5 min * 1 / 0.5 = Max length of 5
# The 5 most recent readings
smoker_deque = deque(maxlen=5) 

# define a callback function to be called when a message is received
def callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # Message is decoded from bytes to a string using decode()
    print(f" [x] Received {body.decode()}")
    reading_string=body.decode()
    # Split the reading_string variable using the split() method
    # Retrieve the second element (index 1) assigned to the 'temp' variable
    try:
        temp=reading_string.split(",")[1]
        smoker_deque.append(float(temp))
        # If there are elements in smoker_deque the code checks if the difference
        # between the max and min values in the deque is greater than or equal to 15.
        # If the condition is met, the code prints a message indicating that the smoker temp has decreased by 15 degrees or more
        if smoker_deque and max(smoker_deque)-min(smoker_deque)>=15:
            print("SMOKER ALERT! Smoker has decreased by 15 degrees or more!")

    # Acknowledge that the message has been processed and can be removed from the queue    
    except ValueError:
        pass
    ch.basic_ack(delivery_tag=method.delivery_tag)
    

# define a main function to run the program
def main(hn: str = "localhost", qn: str = "task_queue"):
    """ Continuously listen for task messages on a named queue."""

    # when a statement can go wrong, use a try-except block
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # If there's an error:
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=qn, durable=True)

        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count=1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume( queue=qn, on_message_callback=callback)

        # print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # If there's an error:
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()
        

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main('localhost', '01-smoker')



