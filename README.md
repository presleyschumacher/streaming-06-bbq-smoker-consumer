## Week 5: Smart Smoker Consumers

> Use RabbitMQ to create 3 consumers that will be used to monitor data from the sensors of a running barbeque smoker. Read one value every 30 seconds

* Smoker-temps.csv has 4 columns:
  * [0] Time = Date-time stamp for the sensor reading
  * [1] Channel1 = Smoker Temp --> send to message queue "01-smoker"
  * [2] Channel2 = Food A Temp --> send to message queue "02-food-A"
  * [3] Channel3 = Food B Temp --> send to message queue "03-food-B"
  
* In week 5, the system will be designed and the producer will be implemented
* In week 6, the consumers will be added and an alert will be raised when interesting events are detected.

## Before You Begin
- [x] Fork this starter repo into your GitHub.
- [x] Clone your repo down to your machine.
- [x] View / Command Palette - then Python: Select Interpreter
- [x] Select your conda environment. 

## Prerequisites
* RabbitMQ Server running
* Pika
* Sys
* Webbrowser
* CSV
* Time

## Usage

> Streaming data is the continuous, constant flow of data being generated and processed. The immediate benefit of the abilities provided by streaming data is the instant feedback when an event, anomaly, or trend begins to occur. In our project example, we are using streaming data to monitor the temperatures of a smoker and the food to ensure everything turns out perfect (or as close to perfect as possible).

1. Sensors
    1. Use temperature sensors to track temperatures and record them to generate a history of both the smoker and the food over time. 

1. Significant Events
    1. We want to know if:
        1. The smoker temperature decreases by more than 15 degrees F in 2.5 minutes
        1. Any food temperature changes less than 1 degree F in 10 minutes
 
 1. Smart System
     1. Use Python to:
         1. Simulate a streaming series of temperature readings from our smart smoker and two foods.
         1. Create a producer to send these temperature readings to RabbitMQ.
         1. Create three consumer processes, each one monitoring one of the temperature streams. 
         1. Perform calculations to determine if a significant event has occurred.
  

## Execution



## Sources
https://www.rabbitmq.com

## Screenshot
