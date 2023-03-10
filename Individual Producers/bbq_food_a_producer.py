""""
    This program sends a message to a queue on the RabbitMQ server from a CSV File to create alert notifications.
    This program is specifically for Food A temperatures
    Author: Presley Schumacher

"""
import pika
import sys
import webbrowser
import csv
import time

def offer_rabbitmq_admin_site(show_offer):
    """Offer to open the RabbitMQ Admin website by using True or False"""
    if show_offer == 'True':
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()

def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.
    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """

# Define the variables
host = "localhost"
food_a_queue = "02-food-A"
data_file = "smoker-temps.csv"

# Define reading in the CSV file
with open(data_file, 'r') as file:
    # Create a csv reader to read per row each new line
    reader = csv.reader(file, delimiter= ',')

    header = next(reader)

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # delete the queue on starup to clear them before initiating them again
        ch.queue_delete(food_a_queue)

        # use the channel to declare a durable queue
        # a durable queue will survive a  server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=food_a_queue, durable=True)
    
        # set the variables for reach column in the row
        for row in reader:
            Time,Channel1,Channel2,Channel3 = row

            # For Smoker, Food_A, and Food_B, the below steps will be followed:
            # use the round() function to round 2 decimal places
            # use the float() function to convert the string to a float
            # use an fstring to create a message from our data
            # prepare a binary message to stream
            # use the channel to publish a message to the queue
        try:
            food_a_channel2 = round(float(Channel2), 2)
            food_a_data = f"{Time}, {food_a_channel2}"
            food_a_message = str(food_a_data).encode()
            ch.basic_publish(exchange="", routing_key=food_a_queue, body=food_a_message)
            print(f" [x] sent {food_a_message}")
        except ValueError:
            pass    
        
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    
    finally:
        # close the connection to the server
        conn.close()

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below

if __name__ == "__main__":
# ask the user if they would like to open the RabbitMQ Admmin
    offer_rabbitmq_admin_site('True')

    send_message('host', 'food_a_queue', 'food_a_message')

    # sleep should be for 30 seconds as the assignment calls
    # we will use 2 seconds for testing and will correct to 30 once we know it is able to run
    time.sleep(2)