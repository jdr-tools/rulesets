import pymodm, os

pymodm.connection.connect(os.getenv('MONGODB_URL'))