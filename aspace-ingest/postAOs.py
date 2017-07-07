import json, requests, csv, time, secrets

startTime = time.time()

# import secrets
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password
repository = secrets.repository

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
# ao_csv = raw_input('Enter csv filename: ')
ao_csv = 'HomewoodPhoto_ASpaceDescription.csv'


# Open csv, create new csv
csv_dict = csv.DictReader(open(ao_csv))
f=csv.writer(open('new_' + ao_csv, 'wb'))
f.writerow(['title']+['dateBegin']+['uri'])

# Construct JSON to post from csv
aoList = []
for row in csv_dict:
	# variables
	title = row['title']
	subject_1 = row['subject1']
	subject_2 = row['subject2']
	date_expression = row['dateExpression']
	date_begin = row['dateBegin']
	agent_2 = row['agentRef2']
	agent_3 = row['agentRef3']
	first_top_container = row['top_container_1']
	first_indicator_2 = row['Disc1']
	second_indicator_2 = row['Disc2']
	second_top_container = row['top_container_2']
	third_indicator_2 = row['Disc3']
	third_top_container = row['top_container_3']
	digital_object = row['digital_object']
	# construct JSON
	aoRecord = {'publish': True, 'title': title, 'level': 'file'}
	# subjects
	if not subject_1 == '' and not subject_2 == '':
		aoRecord['subjects'] = {'ref': '/subjects/138'}, {'ref': subject_1}, {'ref': subject_2}
	elif not subject_1 == '' and subject_2 == '':
		aoRecord['subjects'] = {'ref': '/subjects/138'}, {'ref': subject_1}
	else:
		aoRecord['subjects'] = [{'ref': '/subjects/138'}]
	# dates
	aoRecord['dates'] = [{'expression': date_expression, 'begin': date_begin, 'date_type': 'single', 'label': 'creation'}]
	# linked agents
	if not agent_2 == '' and not agent_3 == '':
		aoRecord['linked_agents'] = {'role': 'creator', 'relator': 'pht', 'ref': 'agents/corporate_entities/388'}, {'role': 'creator', 'relator': 'spn', 'ref': agent_2}, {'role': 'creator', 'relator': 'spn', 'ref': agent_3}
	elif not subject_1 == '' and subject_2 == '':
		aoRecord['subjects'] = {'role': 'creator', 'relator': 'pht', 'ref': 'agents/corporate_entities/388'}, {'role': 'creator', 'relator': 'spn', 'ref': agent_2}
	else:
		aoRecord['subjects'] = [{'role': 'creator', 'relator': 'pht', 'ref': 'agents/corporate_entities/388'}]
	# instances
	# digital objects
	# notes
	# Note: needs to have a linked resource or else NoMethodErro
	aoRecord['resource'] = {'ref': '/repositories/3/resources/1198'}
	aoRecord['parent'] = {'ref': '/repositories/3/archival_objects/154533'}
	aoRecord = json.dumps(aoRecord)
	post = requests.post(baseURL + '/repositories/'+ repository + '/archival_objects', headers=headers, data=aoRecord).json()
	print post
	# # Save uri to new csv file
	# uri = post['uri']
	# f.writerow([title]+[date_begin]+[uri])

# Feedback to user
print 'New .csv saved to working directory.'

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Post complete.  Total script run time: ', '%d:%02d:%02d' % (h, m, s)
