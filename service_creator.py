# This code creates the required kafka topics and PostgreSQL database and also database tables to be used by other scripts.
# Create by Mohammad Hadi Amirsalari , 15-12-2020
# Thanks to https://api.aiven.io/doc/#operation/ServiceKafkaTopicCreate
# Thanks to https://help.aiven.io/en/articles/489573-getting-started-with-aiven-postgresql

import psycopg2
from psycopg2.extras import RealDictCursor
import constants
import http.client
import json
import string

AIVEN_API = constants.AIVEN_API
AIVEN_KAFKA_REST = constants.AIVEN_KAFKA_REST
AIVEN_AUTH_TOKEN = constants.AIVEN_AUTH_TOKEN

TOPIC1 = constants.TOPIC1
TOPIC2 = constants.TOPIC2

DATABASE_URI = constants.DATABASE_URI            # URI Address with desired DB name
DATABASE_SERVICE_URI = constants.DATABASE_SERVICE_URI     # Default URI Address
DATABASE_NAME = constants.DATABASE               # DataBase name
DATABASE_TABLE1 = constants.DATABASE_TABLE1      # DataBase table1 to be used by topic1
DATABASE_TABLE2 = constants.DATABASE_TABLE2      # DataBase table2 to be used by topic2

PAYLOAD = "{\"cleanup_policy\":\"delete\",\"config\":{\"cleanup_policy\":\"delete\",\"compression_type\":\"producer\"," \
          "\"delete_retention_ms\":86400000,\"file_delete_delay_ms\":60000,\"flush_messages\":9223372036854775807," \
          "\"flush_ms\":9223372036854775807,\"index_interval_bytes\":4096,\"max_compaction_lag_ms\":9223372036854775807," \
          "\"max_message_bytes\":1000012,\"message_downconversion_enable\":true,\"message_format_version\":\"2.6-IV0\"," \
          "\"message_timestamp_difference_max_ms\":9223372036854775807,\"message_timestamp_type\":\"CreateTime\"," \
          "\"min_cleanable_dirty_ratio\":0.5,\"min_compaction_lag_ms\":0,\"min_insync_replicas\":1,\"preallocate\":false," \
          "\"retention_bytes\":-1,\"retention_ms\":604800000,\"segment_bytes\":209715200,\"segment_index_bytes\":10485760," \
          "\"segment_jitter_ms\":0,\"segment_ms\":604800000,\"unclean_leader_election_enable\":false},\"min_insync_replicas\":1," \
          "\"partitions\":1,\"replication\":2,\"retention_bytes\":-1,\"retention_hours\":0,\"topic_name\":\"#####\"}"

def check_valid_chars(name):
   if name[0].isdigit():
       return 0
   if len(name) > 249:
       return 0
   allowed_chars=string.digits + string.ascii_lowercase + '_'
   return all(char in allowed_chars for char in name)

def db_connector():
    uri = DATABASE_URI
    db_conn = psycopg2.connect(uri)
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    return cursor,db_conn

def initial_db_connector():
    uri = DATABASE_SERVICE_URI
    db_conn = psycopg2.connect(uri)
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    return cursor,db_conn

# This function is used to create a new database with the desired name already declared in the constants file, in PostgreSQL server.
def database_creator():

    try:
        cursor, db_conn = initial_db_connector()
        db_conn.autocommit = True
        if not check_valid_chars(DATABASE_NAME):
            print("\nPlease only use lowercase alphanumeric characters and underscores for a database name.(max 249 chars starting with a letter)\n")
            exit()
        cursor.execute('CREATE database %s' % DATABASE_NAME)

        # close the database communication
        cursor.close()
        db_conn.close()

        print ('\nThe desired database \"%s\" was created successfully.' % DATABASE_NAME)
    except Exception as ex:
        print('Received Error: ' + str(ex))

# This function is used to create two tables which are already declared in the constants file, in PostgreSQL server.
def table_creator():

    try:
        if not check_valid_chars(DATABASE_TABLE1):
            print("\nPlease only use lowercase alphanumeric characters and underscores for a DB table name.(max 249 chars starting with a letter)\n")
            exit()
        if not check_valid_chars(DATABASE_TABLE2):
            print("\nPlease only use lowercase alphanumeric characters and underscores for a DB table name.(max 249 chars starting with a letter)\n")
            exit()
        cursor, db_conn = db_connector()

        cursor.execute('CREATE TABLE %s (message_id serial PRIMARY KEY, message_text text NOT NULL, message_time timestamp without time zone NOT NULL, offset_id integer)' % DATABASE_TABLE1)
        db_conn.commit()

        cursor.execute('CREATE TABLE %s (message_id serial PRIMARY KEY, message_text text NOT NULL, message_time timestamp without time zone NOT NULL, offset_id integer)' % DATABASE_TABLE2)
        db_conn.commit()

        # close the database communication
        cursor.close()
        db_conn.close()

        print ('\nAll required tables and columns were created successfully.')
    except Exception as ex:
        print('Received Error: ' + str(ex))

# This function is used to create two topics which are already declared in constants file, in kafka server.
def topic_creator():

    try:
        if not check_valid_chars(TOPIC1):
            print("\nPlease only use lowercase alphanumeric characters and underscores for a Kafka topic name.(max 249 chars starting with a letter)\n")
            exit()
        if not check_valid_chars(TOPIC2):
            print("\nPlease only use lowercase alphanumeric characters and underscores for a Kafka topic name.(max 249 chars starting with a letter)\n")
            exit()
        http_connection = http.client.HTTPSConnection(AIVEN_API)
        headers = {
            'content-type': "application/json",
            'Authorization': "Bearer %s" % AIVEN_AUTH_TOKEN
        }
        updated_payload = PAYLOAD.replace('#####', TOPIC1)      # Update topic name inside the payload
        http_connection.request("POST", AIVEN_KAFKA_REST, updated_payload, headers)
        response = http_connection.getresponse()
        status = json.loads(response.read())        # Load json status message response from AIVEN kafka REST service
        if status['message'] == 'created':
            print("\nTopic \"%s\" was successfully created on Kafka server.\n" % TOPIC1)
        else:
            print(status['message'])

        updated_payload = PAYLOAD.replace('#####', TOPIC2)      # Update topic name inside the payload
        http_connection.request("POST", AIVEN_KAFKA_REST, updated_payload, headers)
        response = http_connection.getresponse()
        status = json.loads(response.read())        # Load json status message response from AIVEN kafka REST service
        if status['message'] == 'created':
            print("Topic \"%s\" was successfully created on Kafka server.\n" % TOPIC2)
        else:
            print(status['message'])

    except Exception as ex:
        print('Received Error: ' + str(ex))


if __name__ == '__main__':

    database_creator()
    table_creator()
    topic_creator()
