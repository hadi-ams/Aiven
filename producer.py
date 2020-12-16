
# This code connects to a Kafka server and sends a few randomly generated messages for testing purposes.
# The messages are sent to two different topics, the first one every second and the other one every 2 seconds.
# Create by Mohammad Hadi Amirsalari , 15-12-2020
# Thanks to: https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka

import time
import random
from kafka import KafkaProducer
import constants

# Constants and variables

LANGUAGES = ['JavaScript', 'Python', 'Java', 'C++', 'Swift', 'TypeScript', 'Go Programming Language', 'SQL', 'Ruby'
    , 'R Programming Language', 'PHP', 'Perl', 'Kotlin', 'C#', 'Rust', 'Scheme', 'Erlang', 'Scala', 'Elixir', 'Haskell']

CARS = ['Nissan Rogue', 'Chevrolet Equinox', 'Honda CR-V', 'Toyota RAV4', 'Ford Explorer', 'Ford Escape', 'Jeep Grand Cherokee'
    , 'Toyota Highlander', 'Jeep Wrangler', 'Jeep Cherokee', 'Kia Soul', 'Chevrolet Malibu', 'Ford Fusion', 'Hyundai Elantra', 'Nissan Sentra']

MESSAGE_COUNT = 50      # Total number of sample messages to be sent.
KAFKA_SERVER = constants.KAFKA_SERVER
TOPIC1 = constants.TOPIC1
TOPIC2 = constants.TOPIC2

# Location of SSL authentication certificates
CA_FILE = constants.CA_FILE
CERT_FILE = constants.CERT_FILE
KEY_FILE = constants.KEY_FILE

def producer_function(count):
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            security_protocol='SSL',
            ssl_cafile=CA_FILE,
            ssl_certfile=CERT_FILE,
            ssl_keyfile=KEY_FILE,
        )

        # print(producer.bootstrap_connected())  # check kafka connection status.

        for i in range(0, count):
            # Generate and send some randomly generated JSON messages using "Languages" sample table.
            message_lang = '{"Favorite Language": "%s"}' % LANGUAGES[random.randint(0, 19)]
            print('Sending: {}'.format(message_lang))
            producer.send(TOPIC1, message_lang.encode("utf-8"))

            if (i % 2) == 0:
                # Generate and send some randomly generated JSON messages using "Cars" sample table. (Every 2 seconds)
                message_car = '{"Favorite Car": "%s"}' % CARS[random.randint(0, 14)]
                print('Sending: {}'.format(message_car))
                producer.send(TOPIC2, message_car.encode('utf-8'))

            time.sleep(1) # add a 1 second delay

        # Force sending of all messages
        producer.flush()
    except Exception as ex:
        print('Received Error: ' + str(ex))

if __name__ == '__main__':

    producer_function(MESSAGE_COUNT)
