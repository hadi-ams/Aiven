
# This code tests the communication between a kafka server and a PostgreSQL DataBase.
# Please refer to script options for further information.
# Create by Mohammad Hadi Amirsalari , 15-12-2020
# Thanks to: https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka
# Thanks to: https://help.aiven.io/en/articles/489573-getting-started-with-aiven-postgresql

from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import psycopg2
from psycopg2.extras import RealDictCursor
import constants
import cmd

# Constants and variables

KAFKA_SERVER = constants.KAFKA_SERVER
TOPIC = ''

TEST_PARTITION = 0

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


def producer_function():
	producer = KafkaProducer(
		bootstrap_servers=KAFKA_SERVER,
		security_protocol='SSL',
		ssl_cafile=CA_FILE,
		ssl_certfile=CERT_FILE,
		ssl_keyfile=KEY_FILE,
	)
	return producer

def consumer_function():
	consumer = KafkaConsumer(
		auto_offset_reset='earliest',
		bootstrap_servers=KAFKA_SERVER,
		client_id='user1',
		group_id='group1',
		security_protocol='SSL',
		ssl_cafile=CA_FILE,
		ssl_certfile=CERT_FILE,
		ssl_keyfile=KEY_FILE,
	)
	return consumer

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

def test_selector():

	print ('\nSelect the test type and enter the desired number:\n\n'
		   '1)Test the connection to PostgreSQL DataBase\n'
		   '2)Test the connection to Kafka server\n'
		   '3)Test the message flow process between Kafka and DataBase\n'
		   '4)Create sample scenario where: last message was submitted to DB but not committed to Kafka\n'
		   '5)Create sample scenario where: last message was not submitted to DB but committed to Kafka\n')

	option = input('')  # Python 3

	if option == '1':
		try:
			last_row = 'No data has been saved in the DataBase yet.'
			cursor, db_conn = db_connector()
			cursor.execute('SELECT current_database()')
			result = cursor.fetchone()
			current_database = list(result.items())[0][1]
			cursor.execute('SELECT * from %s order by message_id desc limit 1' % DATABASE_TABLE)
			result = cursor.fetchone()
			if result:
				last_row = list(result.items())
			if cursor.closed:
				print('\nDataBase Server is not available.')
			else:
				cursor.close()
				db_conn.close()
				print('\nDataBase Server is available and operational.'
					  '\nYou are connected to the following DataBase:\n\n%s'
					  '\n\nThe last row in the table \"%s\" which corresponds to \"%s\" topic is:\n\n%s' % (current_database, DATABASE_TABLE, TOPIC, last_row))
		except Exception as ex:
			print('\nDataBase Server is not available.')
			print('Received Error: ' + str(ex))
		finally:
			print('\n## Test is finished ##')

	elif option == '2':
		try:
			producer = producer_function()
			consumer = consumer_function()
			topics = consumer.topics()		# Get a list of accessible topics
			topic_partition = TopicPartition(TOPIC, TEST_PARTITION)
			consumer.assign([topic_partition])		# Assign a new consumer topic and partition
			assignment = consumer.assignment()		# Get the currently assigned partition
			if producer.bootstrap_connected():
				print('\nKafka Server is available and operational. You have access to the following topics:\n\n%s\n\nAnd the following partition:\n\n%s' % (topics, assignment))
			else:
				print('\nKafka Server is not available.')
		except Exception as ex:
			print('\nKafka Server is not available.')
			print('Received Error: '+ str(ex))
		finally:
			print ('\n## Test is finished ##')

	elif option == '3':
		try:
			producer = producer_function()
			consumer = consumer_function()
			topics = consumer.topics()		# Get a list of accessible topics

			if producer.bootstrap_connected():
				print('\nKafka Server is available and operational. You have access to the following topics:\n\n%s\n' % topics)
			else:
				print('\nKafka Server is not available.')

			topic_partition = TopicPartition(TOPIC, TEST_PARTITION)		# Create topic partition object
			consumer.assign([topic_partition])		# Assign a new consumer topic and partition
			next_offset = consumer.position(topic_partition)		# Get the next Offset to be loaded from Kafka
			end_offset = consumer.end_offsets([topic_partition])	# Get end Offset for next message in Kafka

			print ('End Offset for next message in Kafka (Topic: %s ): ' % TOPIC + str(end_offset[topic_partition]))
			print ('Next Offset to be loaded from Kafka (Topic: %s ): ' % TOPIC + str(next_offset))

			cursor, db_conn = db_connector()
			cursor.execute('SELECT offset_id from %s order by message_id desc' % DATABASE_TABLE)
			result = cursor.fetchone()
			if result:
				db_offset_id = list(result.items())[0][1]
			else:
				db_offset_id = -1

			print ('Last offset saved in DB (Table: %s ): ' % DATABASE_TABLE + str(db_offset_id))
			print ('\nThere are %s new message[s] available to consume (Topic: %s ). (lag)' % (str(end_offset[topic_partition] - next_offset), TOPIC))

			cursor.close()
			db_conn.close()

			if next_offset == db_offset_id+1:
				print('\nKafka and DB are in perfect sync and messages are saved properly.')
			else:
				print('\n!!!! Kafka and DB are not in sync and there is a discrepancy. !!!!')

		except Exception as ex:
			print('\nKafka Server or DataBase server is not available.')
			print('Received Error: '+ str(ex))
		finally:
			print ('\n## Test is finished ##')

	elif option == '4':
		try:
			cursor, db_conn = db_connector()
			# Increase offset id for last message saved in DataBase.
			cursor.execute('UPDATE %s set offset_id = offset_id +1 where message_id IN (SELECT max(message_id) FROM %s)' % (DATABASE_TABLE, DATABASE_TABLE))
			db_conn.commit()
			print('\nChanges were submitted to DB. You can try test option 3 now.')
		except Exception as ex:
			print('\nDataBase Server is not available.')
			print('Received Error: ' + str(ex))
		finally:
			print('\n## Test is finished ##')

	elif option == '5':
		try:
			cursor, db_con = db_connector()
			# Decrease offset id for last message saved in DataBase.
			cursor.execute('UPDATE %s set offset_id = offset_id -1 where message_id IN (SELECT max(message_id) FROM %s)' % (DATABASE_TABLE, DATABASE_TABLE))
			db_con.commit()
			print('\nChanges were submitted to DB. You can try test option 3 now.')
		except Exception as ex:
			print('\nDataBase Server is not available.')
			print('Received Error: ' + str(ex))
		finally:
			print('\n## Test is finished ##')
	else:
		print ('\nInvalid option. Please try again.')
		test_selector()

if __name__ == '__main__':

	topic_selector()
	test_selector()