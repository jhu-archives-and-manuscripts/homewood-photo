import json, requests, csv, time, secrets
from datetime import datetime

# import secrets
secretsVersion = raw_input('To edit production server, enter the name of the secrets file: ')
if secretsVersion != '':
    try:
        secrets = __import__(secretsVersion)
        print 'Editing Production'
    except ImportError:
        print 'Editing Development'
else:
    print 'Editing Development'

startTime = time.time()

baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

# test for successful connection
def test_connection():
	try:
		requests.get(baseURL)
		print 'Connected!'
		return True

	except requests.exceptions.ConnectionError:
		print 'Connection error. Please confirm ArchivesSpace is running.  Trying again in 10 seconds.'

is_connected = test_connection()

while not is_connected:
	time.sleep(10)
	is_connected = test_connection()

#authenticate
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

# User supplied variables
agents_csv = raw_input('Enter csv filename: ')

# Open csv, create new csv

date = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
csv_dict = csv.DictReader(open(agents_csv))
f=csv.writer(open(date + 'new_' + agents_csv, 'wb'))
f.writerow(['primary_name']+['subordinate_name_1']+['uri'])

# Construct JSON to post from csv
agentList = []
for row in csv_dict:
    primary_name = row['primary_name']
    subordinate_name_1 = row['subordinate_name_1']
    agentRecord = {'publish': True}
    agentRecord['names'] = [{'primary_name': primary_name, 'sort_name': primary_name + '. ' + subordinate_name_1, 'subordinate_name_1': subordinate_name_1, 'source': 'local', 'rules': 'rda'}]
    agentRecord = json.dumps(agentRecord)
    post = requests.post(baseURL + '/agents/corporate_entities', headers=headers, data=agentRecord).json()
    print post
    # Save uri to new csv file
    uri = post['uri']
    f.writerow([primary_name]+[subordinate_name_1]+[uri])

# Feedback to user
print 'New .csv saved to working directory.'

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Post complete.  Total script run time: ', '%d:%02d:%02d' % (h, m, s)
