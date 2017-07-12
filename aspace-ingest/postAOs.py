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
ao_csv = raw_input('Enter csv filename: ')
resource_record = raw_input('Enter resource record uri: ')
parent_series = raw_input('Enter parent series uri: ')

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
	first_indicator_1 = row['Box1']
	first_indicator_2 = row['Disc1']
	second_top_container = row['top_container_2']
	second_indicator_1 = row['Box2']
	second_indicator_2 = row['Disc2']
	third_top_container = row['top_container_3']
	third_indicator_1 = row['Box3']
	third_indicator_2 = row['Disc3']
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
		aoRecord['linked_agents'] = {'role': 'creator', 'relator': 'pht', 'ref': '/agents/corporate_entities/388'}, {'role': 'creator', 'relator': 'spn', 'ref': agent_2}, {'role': 'creator', 'relator': 'spn', 'ref': agent_3}
	elif not agent_2 == '' and agent_3 == '':
		aoRecord['linked_agents'] = {'role': 'creator', 'relator': 'pht', 'ref': '/agents/corporate_entities/388'}, {'role': 'creator', 'relator': 'spn', 'ref': agent_2}
	else:
		aoRecord['linked_agents'] = [{'role': 'creator', 'relator': 'pht', 'ref': '/agents/corporate_entities/388'}]
	# instances
	# if not second_top_container == '' and not third_top_container == '':
 # 		container = {'type_1': 'box', 'indicator_1': first_indicator_1, 'type_2': 'item', 'indicator_2': first_indicator_2}, {'type_1': 'box', 'indicator_1': second_indicator_1, 'type_2': 'item', 'indicator_2': second_indicator_2}, {'type_1': 'box', 'indicator_1': third_indicator_1, 'type_2': 'item', 'indicator_2': third_indicator_2}
	# 	sub_container = {'type_2': 'item', 'indicator_2': first_indicator_2}, {'type_2': 'item', 'indicator_2': second_indicator_2}, {'type_2': 'item', 'indicator_2': third_indicator_2}
	# 	sub_container['top_container'] = {'ref': first_top_container}, {'ref': second_top_container}, {'ref': third_top_container}
	# 	aoRecord['instances'] = [{'instance_type': 'mixed_materials', 'sub_container': sub_container, 'container': container}]
	# # elif not second_top_container == '' and third_top_container == '':
	# # 	container = {'type_1': 'box', 'indicator_1': first_indicator_1, 'type_2': 'item', 'indicator_2': first_indicator_2}, {'type_1': 'box', 'indicator_1': second_indicator_1, 'type_2': 'item', 'indicator_2': second_indicator_2}
	# # 	sub_container = {'type_2': 'item', 'indicator_2': first_indicator_2}, {'type_2': 'item', 'indicator_2': second_indicator_2}
	# # 	sub_container['top_container'] = {'ref': first_top_container}, {'ref': second_top_container}
	# # 	aoRecord['instances'] = [{'instance_type': 'mixed_materials', 'sub_container': sub_container, 'container': container}]
	if not first_top_container == '':
		container = {'type_1': 'box', 'indicator_1': first_indicator_1, 'type_2': 'item', 'indicator_2': first_indicator_2}
		sub_container = {'type_2': 'item', 'indicator_2': first_indicator_2}
		sub_container['top_container'] = {'ref': first_top_container}
		aoRecord['instances'] = [{'instance_type': 'mixed_materials', 'sub_container': sub_container, 'container': container}]
	# # digital objects
	# notes
	# resource and parent
	# Note: needs to have a linked resource or else NoMethodError
	aoRecord['resource'] = {'ref': '/repositories/3/resources/' + resource_record}
	aoRecord['parent'] = {'ref': '/repositories/3/archival_objects/' + parent_series}
	aoRecord = json.dumps(aoRecord)
	post = requests.post(baseURL + '/repositories/'+ repository + '/archival_objects', headers=headers, data=aoRecord).json()
	print post
	# Save uri to new csv file
	uri = post['uri']
	f.writerow([title]+[date_begin]+[uri])

# Feedback to user
print 'New .csv saved to working directory.'

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Post complete.  Total script run time: ', '%d:%02d:%02d' % (h, m, s)
