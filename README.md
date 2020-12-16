# Introduction

This project is a demo application for getting familiar with Aiven (www.aiven.io) services.

The basic idea is that a producer function will be sending randomly generated JSON messages to two different Kafka topics which were created earlier on an Aiven Kafka service. Later on a consumer function will connect to the Kafka service and load those messages and save them in a PostgreSQL database which was earlier created on Aiven cloud.
The consumer function is capable of connecting to each topic separately and update the corresponding database table.

There is a test script which handles different test scenarios and is capable of testing each topic separately.

Please follow the rest of this tutorial for further information.

# Project setup guide and prerequisites

This project is using "Python3" as the programming language and was originally tested on a Debian machine. Hence the setup instructions are for Debian distro but it must be fairly easy to extend it to other distros.
Please open a terminal window and start with installing the following dependencies and modules:

```
sudo su
apt update
apt full-upgrade
apt install python3-pip
apt install libpq-dev
apt install libcurl4-openssl-dev libssl-dev

pip3 inatall kafka-python
pip3 install psycopg2
pip3 install http.client
```

Brief intro:  

`python3-pip` : Python3 module installer  
`libpq-dev` : Required for PostgreSQL python driver module `psycopg2` to be installed  
`libcurl4-openssl-dev` and `libssl-dev` : Required for `http.client` module to be installed  
  
`kafka-python` : Required for communication with Kafka instance  
`psycopg2` : Required for communication with PostgreSQL instance  
`http.client` : Required for communication with Aiven REST api  

# Aiven service setup guide

In order to take advantage of this project and get familiar with Aiven services you need to have an Aiven cloud account so you can create required services.  
You can either purchase a subscription or sign up for a 1 month trial account.
To register for a demo account please register to Aiven at https://console.aiven.io/signup.html at which point you'll automatically be given $300 worth of credits to create and test a few services for a while. This should be enough for several hours use of Aiven services.
After signing up and successfully validating your Email address you will have access to your account dashboard (https://console.aiven.io/project).  
A new project is automatically created for you. Please note the project name at the top left side of the page and save it for later use.  

## Kafka service setup

Please note the top right button 'Create a new service' and click to proceed.  
On the next page you have options to configure your Kafka instance.  
You can use these suggested configurations:  
1) Kafka Version 2.6  
2) Google Cloud Platform  
3) USA Region
4) Service Plan : startup
5) Either provide a service name or use the automatically created name.  

Please save the service name for later use.  
Finally hit create service on the right bottom side and be patient for a few minutes until the system is finished setting up your Kafka instance and status under the service name is changed from "REBUILDING" to "RUNNING".  

Now click on the service and look at the overview page:  
There are a few important information that you need to save for later use:  
1) Copy and save the "Service URI"
2) Download all 3 certificates : `Access Key` , `Access Certificate` and `CA Certificate` and save them to the root of your desired project folder on your hard disk.  

Now we are done with setting up and preparing the requirements for the Kafka instance. Please proceed to the next step.

## PostgreSQL service setup

Go back to the Aiven dashboard and hit create a new service.  
You can select the following suggested configurations:
1) PostgreSQL Version 12
2) Google Cloud Platform  
3) USA Region
4) Service Plan : hobbyist
5) Either provide a service name or use the automatically created name.  

Finally hit create service on the right bottom side and be patient for a few minutes until the system is finished setting up your PostgreSQL instance and status under the service name is changed from "REBUILDING" to "RUNNING".  

Now click on the service and look at the overview page:  
There is an important information that you need to save for later use:  
1) Copy and save the "Service URI"

Now we are done with setting up and preparing the requirements for the PostgreSQL instance. Please proceed to the next step.

## Generating authentication token

In order to get use of the Aiven REST api we need to have an authentication token.  
Please go back to the Aiven dashboard and notice the "User information" icon on the top right side of the page and click on it.  
On the next page go to the second tab: "Authentication".  
Scroll down and click on the "Generate token" button on the bottom left side.  
Give it your desired description and leave the next box empty and click "Generate token".  
On the next page please copy and save the generated token for later use.  

Now we are done with all the steps required for Aiven service setup and we can proceed to the project setup/running.

# Configuring and running the project

Please clone or download all the project files and save them to the root of your project folder.  
After doing so your project folder should include all the following files:  
* constants.py
* consumer.py
* producer.py
* service_creator.py
* tests.py
  
* service.cert
* service.key
* ca.pem
  
 Reminder: The certificates were downloaded at an earlier stage from the Aiven Kafka instance overview page.  
 
 ## Configuring the constants file
 
 Please open the file `constants.py` with your suitable text editor and update the following fields:  
   
 * `AIVEN_AUTH_TOKEN` : Update it with the previously generated authentication token.
 * `AIVEN_PROJECT` : Update it with the project name which you saved it before.
 * `AIVEN_KAFKA_SERVICE` : Update it with the Aiven Kafka service name (Not URI).
 * `KAFKA_SERVER` : Update it with the Kafka service URI.
 * `TOPIC1` : Choose a topic name of your choosing. It can be anything you like. You can leave it as it is.
 * `TOPIC2` : Choose a second topic name of your choosing. It can be anything you like. You can leave it as it is.
 * `CA_FILE`, `CERT_FILE`, `KEY_FILE` : You don't need to update them as long as the certificates are in the same folder as the scripts or otherwise provide the correct location for the certificates.
 * `DATABASE` : Choose a DataBase name of your choosing. It can be anything you like. You can leave it as it is.
 * `DATABASE_SERVICE_URI` : Update it with the PostgreSQL service URI.
 * `DATABASE_TABLE1` : Choose a table name of your choosing. It can be anything you like. You can leave it as it is.
 * `DATABASE_TABLE2` : Choose a second table name of your choosing. It can be anything you like. You can leave it as it is.  
 
 Please be careful to only use alphanumeric lowercase characters and underscores for Kafka topic, table and database names. (max 249 chars starting with a letter)  
 Now the initial configuration of the project is done and everything is in order, to start running the project and testing it.  
 
 ## Running and testing the project files and scripts
 
 In order to run any of the main project files you need to be at a Linux (Debian) terminal with the working directory at the project root folder.  
 In order to run the scripts initiate the following command: `python3 FILE_NAME.py`  
 We will start going through the functions and files one by one in order of functionality:
 
 ### service_creator.py
 
 `python3 service_creator.py`
 
 This is a helper script for creating the required DataBase, DataBase tables and columns and also Kafka Topics on the Aiven cloud servers. You can either use this helper script or create them manually on the cloud for advanced configuration and setup. You also have the chance to modify the configurations directly from the helper script.  
 Once you run the script if everything is configured properly according to previous tutorial steps you should see something like the following success messages:  
 
 ```
The desired database "info" was created successfully.

All required tables and columns were created successfully.

Topic "langs" was successfully created on Kafka server.

Topic "cars" was successfully created on Kafka server.
```
The created DataBase will have two tables with the names defined in the constants file.  
Each table will have the following 4 columns in order to store our sample data:  
* `message_id` : This is the primary key for the table and is a serial sequence.
* `message_text` : This is where the actual JSON message is stored in text format.
* `message_time` : This is time stamp of the message when it was stored on the Kafka server.
* `offset_id` : This is the offset_id of the message on the Kafka server.
  
 The created Kafka topics will have all the default configurations assigned by Aiven which you can further investigate them by having a look at the Kafka service in the Aiven dashboard.  The topics are created by using and integrating the Aiven REST api, to the project using the authentication token.
 The most important things about the topics are that for the sake of simplicity of the project they both have only one partition and a replication factor of two.

 ### producer.py
 
 `python3 producer.py`  
 
 The producer function is responsible for creating some randomly generated JSON messages to mimic a scenario where supposedly there is a website or service with two different kinds of information about favorite cars and favorite programming languages which random users select from them.  
 To realize the idea there are two sample lists with pre-filled information about favorite cars and programming languages which the code randomly chooses from the list and creates JSON messages to send to the Kafka service and stores them there.  
 There is a constant MESSAGE_COUNT with default value of 50, defined at the beginning of the code which defines the number of messages sent, which you can change it to your liking. By default the code is sending one favorite language per second and one favorite car every two seconds.  
 The favorite language messages will be sent to the first created topic and the favorite car messages will be sent to the second topic on Kafka service.
 If everything works fine and previous steps are done properly you should see some output like the following which will continue until almost 50 seconds:  
```
Sending: {"Favorite Language": "Python"}
Sending: {"Favorite Car": "Ford Escape"}
Sending: {"Favorite Language": "C++"}
Sending: {"Favorite Language": "Rust"}
Sending: {"Favorite Car": "Ford Explorer"}
.  
.  
.  
```

 ### consumer.py
 
 `python3 consumer.py`  
 
 The consumer function is responsible for consuming (fetching) the messages from the Kafka service and store them on the Aiven PostgreSQL service.  
 Upon running the script you will see a topic selection prompt which will ask you about the topic you want to consume and you have to respond accordingly by entering the desired option as a number.  
 ```
 
Select the desired topic and enter the desired number:

1)langs

2)cars

 ```
 Let's say you selected the first topic and pressed enter. You should be seeing the following messages after a few seconds:  
 
 ```
Received: {"Favorite Language": "Python"}
Received: {"Favorite Language": "C++"}
Received: {"Favorite Language": "Rust"}
 ```
 
 This means that the messages were successfully consumed and received from the Kafka service and were saved to the corresponding DataBase table on the cloud.  
 You can repeat the same process for the second topic.
 
 ## TESTS
 
 The following describes different testing scenarios and how the test script works for different functionalities.
 
 ### tests.py
 
 `python3 tests.py`  
 
 After running the script, similar to the consumer script you will be faced with the topic selection prompt which will give you the chance to select your desired topic for starting the test process.  
 After selecting your desired topic you should see the following selection choices which will be explained one by one:  
  ```
  
Select the test type and enter the desired number:

1)Test the connection to PostgreSQL DataBase
2)Test the connection to Kafka server
3)Test the message flow process between Kafka and DataBase
4)Create sample scenario where: last message was submitted to DB but not committed to Kafka
5)Create sample scenario where: last message was not submitted to DB but committed to Kafka

  ```

* Option 1 :   

This option will test your connection to the PostgreSQL database service and if everything is alright you should be seeing something similar to the following messages:  

```

DataBase Server is available and operational.
You are connected to the following DataBase:

info

The last row in the table "favorite_languages" which corresponds to "langs" topic is:

[('message_id', 3), ('message_text', '{"Favorite Language": "Rust"}'), ('message_time', datetime.datetime(2020, 12, 16, 7, 47, 12, 385000)), ('offset_id', 2)]

## Test is finished ##
```

* Option 2 :  

This will test your connection to the Aiven Kafka service for the selected topic and if everything is alright you should be seeing something like the following messages:  

```
Kafka Server is available and operational. You have access to the following topics:

{'cars', 'langs'}

And the following partition:

{TopicPartition(topic='langs', partition=0)}

## Test is finished ##  
```

* Option 3 :  

This option is responsible for making sure the message flow process between Kafka and PostgreSQL database is working properly.  
Upon selecting this option if everything is alright you should be seeing some messages like the following:  
```

Kafka Server is available and operational. You have access to the following topics:

{'cars', 'langs'}

End Offset for next message in Kafka (Topic: langs ): 7
Next Offset to be loaded from Kafka (Topic: langs ): 3
Last offset saved in DB (Table: favorite_languages ): 2

There are 4 new message[s] available to consume (Topic: langs ). (lag)

Kafka and DB are in perfect sync and messages are saved properly.

## Test is finished ##
```  

In the case that there might be an issue and the two services are not in sync which we have a chance to create in options 4 and 5, or by interrupting the consumer script before it has completely finished doing it's job, after selecting option 3 you will be seeing something like the following messages:  
```

Kafka Server is available and operational. You have access to the following topics:

{'langs', 'cars'}

End Offset for next message in Kafka (Topic: langs ): 7
Next Offset to be loaded from Kafka (Topic: langs ): 3
Last offset saved in DB (Table: favorite_languages ): 3

There are 4 new message[s] available to consume (Topic: langs ). (lag)

!!!! Kafka and DB are not in sync and there is a discrepancy. !!!!

## Test is finished ##
```  

* Option 4 :  

This option is responsible for creating a sample scenario where the last message was submitted to DB but not committed to Kafka and the offset in the DataBase is one more than it should be.  
After selecting this option you should be seeing something like the following messages:   
```

Changes were submitted to DB. You can try test option 3 now.

## Test is finished ##
```  

Please remember in order to actually test this scenario you need to run the test script again and check message flow process by selecting the option 3.  


* Option 5 :  

This option is responsible for creating a sample scenario where the last message was not submitted to DataBase but was committed to Kafka and the offset in the DataBase is one less than it should be.  
After selecting this option you should be seeing something like the following messages:   
```

Changes were submitted to DB. You can try test option 3 now.

## Test is finished ##
```  

Please remember in order to actually test this scenario you need to run the test script again and check message flow process by selecting the option 3.  

* Please remember that options 4 and 5 work exactly opposite to each other and they cancel out each other's effect. So if you run them consecutively you will be back to the normal working scenario.  

