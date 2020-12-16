
# This code connects to a Kafka server and receives messages from a Kafka topic and submits them to a PostgreSQL DataBase.
# To try consuming messages from another topic please change the corresponding topics and DB tables in the constants area.
# Create by Mohammad Hadi Amirsalari , 15-12-2020
# Thanks to: https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka
# Thanks to: https://help.aiven.io/en/articles/489573-getting-started-with-aiven-postgresql

from kafka import KafkaConsumer, TopicPartition
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import constants
import cmd

# Constants and variables

KAFKA_SERVER = constants.KAFKA_SERVER
TOPIC = ''

# Location of SSL authentication certificates
CA_FILE = constants.CA_FILE
CERT_FILE = constants.CERT_FILE
KEY_FILE = constants.KEY_FILE

DATABASE = constants.DATABASE
DATABASE_URI = constants.DATABASE_URI
DATABASE_TABLE = ''

def db_connector():
    uri = DATABASE_URI
    db_conn = psycopg2.connect(uri)
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    return cursor,db_conn

def topic_selector():

    global DATABASE_TABLE
    global TOPIC
    print ('\nSelect the desired topic and enter the desired number:\n\n'
		   '1)%s\n\n'
		   '2)%s\n' % (constants.TOPIC1, constants.TOPIC2))

    option = input('')  # Python 3

    if option == '1':
        DATABASE_TABLE = constants.DATABASE_TABLE1
        TOPIC = constants.TOPIC1
    elif option == '2':
        DATABASE_TABLE = constants.DATABASE_TABLE2
        TOPIC = constants.TOPIC2
    else:
        print ('\nInvalid option. Please try again.')
        topic_selector()
    return

def consumer_function():

    try:
        consumer = KafkaConsumer(
            TOPIC,
            auto_offset_reset='earliest',
            bootstrap_servers=KAFKA_SERVER,
            client_id='user1',
            group_id='group1',
            security_protocol='SSL',
            ssl_cafile=CA_FILE,
            ssl_certfile=CERT_FILE,
            ssl_keyfile=KEY_FILE,
        )
        # print(consumer.bootstrap_connected()) # check kafka connection status.

        # Call poll twice. First call will just assign partitions for our
        # consumer without actually returning anything
        for _ in range(2):
            raw_msgs = consumer.poll(timeout_ms=1000)
            for tp, msgs in raw_msgs.items():

                cursor,db_conn = db_connector()
                for msg in msgs:
                    message_text = msg.value.decode('utf-8')
                    print('Received: {}'.format(message_text))
                    # Convert to suitable time stamp format accepted by PostgreSQL
                    converted_time = datetime.fromtimestamp(msg.timestamp/ 1000)
                    # Save received message into corresponding database table including message text, time stamp and offset id.
                    cursor.execute("insert into %s (message_text, message_time, offset_id) values ('%s', '%s', %d)" % (DATABASE_TABLE ,message_text, converted_time, msg.offset))

                db_conn.commit()
                # close the database communication
                cursor.close()
                db_conn.close()
        # Commit offsets so we won't get the same messages again
        consumer.commit()
    except Exception as ex:
        print('Received Error: ' + str(ex))

if __name__ == '__main__':

    topic_selector()
    consumer_function()
