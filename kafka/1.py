from confluent_kafka import Producer
from faker import Faker
import random
from transliterate import translit, get_available_language_codes
import hashlib

#p = Producer({'bootstrap.servers':'10.182.19.20:29092'})
# Initialize the Kafka producer with SASL_SSL authentication

p = Producer({
    'bootstrap.servers': '10.182.19.20:29092',
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.username': 'admin',
    'sasl.password': 'admin-secret',
})
def make_message():

  fake = Faker("ru_RU")
  gender=random.choice(['M','F'])
  name=''
  last=''
  if gender=='M':
      last_name=fake.last_name_male()
      name=fake.first_name_male()
  else:
      last_name=fake.last_name_female()
      name=fake.first_name_female()
  tr_lastname=translit(last_name, 'ru',reversed=True).upper().replace("'","")
  tr_name=translit(name, 'ru',reversed=True).upper().replace("'","")

  delimiters=['.','_','-']
  m = hashlib.sha256()
  num=random.choice([random.randint(1970,2010),''])
  email='{}{}{}{}@{}'.format (tr_name.lower(), random.choice(delimiters),tr_lastname.lower(),num,fake.hostname())
  phone=fake.phone_number()
  full='{} {}'.format(tr_name,tr_lastname)
  m.update(bytes(full ,'UTF8'))
  id=m.hexdigest()[:6].upper()
  id2='0005432799170'
  dop={"email": email, "phone": phone}
  message=f"{id2}\t{id}\t{full}\t{str(dop)}"
  return message
#print (id,full,email,phone)
def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
#some_data_source=[
#    '0005432799170	0FB29D	ANGELINA SMIRNOVA	{"email": "smirnova-angelina-121966@postgrespro.ru", "phone": "+70769619399"}' ,
#    ]
#csv_file="table_csv_f6ece0a9a33044f7-b10acb7ae8b12063_0.csv"
#f=open(csv_file)
#some_data_source=f.readlines()
some_data_source=[]
fake = Faker("ru_RU")
for i in range(80):
  #if i%3==0:
  #some_data_source.append(make_message()  )
  #else:
  some_data_source.append(make_message()+f"\t{fake.company()}"  )
f=open('test5.csv','w')

for data in some_data_source:
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)
    print(data)
    # Asynchronously produce a message. The delivery report callback will
    # be triggered from the call to poll() above, or flush() below, when the
    # message has been successfully delivered or failed permanently.
    f.write(data+'\n')

    p.produce('doris3', data.encode('utf-8'), callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()
f.close()
