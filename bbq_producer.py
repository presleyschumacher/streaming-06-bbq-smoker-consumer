"""
    This program sends a message to a queue on the RabbitMQ server from a CSV File to create alert notifications.

    Author: Presley Schumacher
    Date: February 14, 2023

"""

import pika
import sys
import webbrowser
import csv
import time

# Define the variables
host = "localhost"
smoker_queue = "01-smoker"
food_a_queue = "02-food-A"
food_b_queue = "02-food-B"
data_file = "smoker-temps.csv"

def offer_rabbitmq_admin_site(show_offer):
    """Offer to open the RabbitMQ Admin website by using True or False"""
    if show_offer == True:
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()

def delete_queue(host: str, queue_name: str):
    """
    Delete queues each time we run the program
    """
    conn = pika.BlockingConnection(pika.ConnectionParameters(host))
    ch = conn.channel()
    ch.queue_delete(queue=queue_name)

def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.
    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """
    try:
         # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a  server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        print(f" [x] Sent {message} on {queue_name}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

# Define reading in the CSV file 
def csv_file(data_file):
    with open(data_file, "r") as file:
        # create a csv reader for our comma delimited data
        reader = csv.reader(file, delimiter=",")
        # skipping header row
        next(reader)
        for row in reader:
            fstring_time_column = f"{row[0]}"
    
        # For Smoker, Food_A, and Food_B, the below steps will be followed:
        # some of the columns are numbers so we need to convert them to floats
        # If the value can be converted to a float, a string message will be constructed
        # If it cannot be converted into a float, it will move onto the next row
        # Send the message to the message queue
        try:
            smoker_channel1 = float(row[1])
            smoker_data = (fstring_time_column, smoker_channel1)
            smoker_message = str(smoker_data).encode()
            send_message(host, smoker_queue, smoker_message)
        except ValueError:
            pass

        try:
            food_a_channel2 = float(row[2])
            food_a_data = {fstring_time_column, food_a_channel2}
            food_a_message = str(food_a_date).encode()
            send_message(host, food_a_queue, food_a_message)
        except ValueError:
            pass    

        try:
            food_b_channel3 = float(row[3])
            food_b_data = {fstring_time_column, food_b_channel3}
            food_b_message = str(food_b_date).encode()
            send_message(host, food_b_queue, food_b_message)
        except ValueError:
            pass

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # ask the user if they would like to open the RabbitMQ Admmin
    offer_rabbitmq_admin_site('true')

    # Send Messages
    send_message('localhost',"smoker_queue", "smoker_message")
    send_message('localhost',"food_a_queue", "food_a_message") 
    send_message('localhost',"food_b_queue", "food_b_message")

    # Sleep for 30 seconds
    time.sleep(30)