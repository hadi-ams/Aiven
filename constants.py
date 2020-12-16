# Constants and variables
# Create by Mohammad Hadi Amirsalari , 15-12-2020

AIVEN_AUTH_TOKEN = ''

AIVEN_PROJECT = ''
AIVEN_KAFKA_SERVICE = ''
AIVEN_API = 'api.aiven.io'
AIVEN_KAFKA_REST = '/v1/project/'+AIVEN_PROJECT+'/service/'+AIVEN_KAFKA_SERVICE+'/topic'

KAFKA_SERVER = ''
TOPIC1 = 'langs'        # Your desired topic1 name
TOPIC2 = 'cars'         # Your desired topic2 name

# Location of SSL authentication certificates
CA_FILE = 'ca.pem'
CERT_FILE = 'service.cert'
KEY_FILE = 'service.key'

DATABASE = 'info'       # Name of desired DataBase on the cloud
DATABASE_SERVICE_URI = ''
DATABASE_URI = DATABASE_SERVICE_URI.replace('defaultdb', DATABASE)
DATABASE_TABLE1 = 'favorite_languages'      # Your desired table1 name
DATABASE_TABLE2 = 'favorite_cars'           # Your desired table2 name
