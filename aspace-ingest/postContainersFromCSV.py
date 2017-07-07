# This script works to create instances (consisting of top_containers) from a separate CSV file. The CSV file should have two columns, indicator and barcode.
# The directory where this file is stored must match the directory in the filePath variable, below.
# The script will prompt you first for the exact name of the CSV file, and then for the exact resource or accession to attach the containers to.

import json, requests, secrets, csv, time

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

# User supplied variables name of csv
container_csv = raw_input('Enter csv filename: ')
collection = raw_input('Enter resource record uri: ')
container_profile = raw_input('Enter container profile uri: ')

# Open csv, create new csv
csv_dict = csv.DictReader(open(container_csv))
f=csv.writer(open('new_' + container_csv, 'wb'))
f.writerow(['indicator']+['barcode']+['uri'])

containerList = []
for row in csv_dict:
    barcode = row['barcode']
    indicator = row['indicator']
    containerRecord = {'barcode': barcode, 'indicator': indicator}
    containerRecord['collection'] = [{'ref': '/repositories/' + repository + '/resources/' + collection}]
    containerRecord['container_profile'] = {'ref': '/container_profiles/' + container_profile}
    containerRecord = json.dumps(containerRecord)
    post = requests.post(baseURL + '/repositories/'+ repository + '/top_containers', headers=headers, data=containerRecord).json()
    print post
    # Save uri to new csv file
    uri = post['uri']
    f.writerow([indicator]+[barcode]+[uri])

# Feedback to user
print 'New .csv saved to working directory.'

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Post complete.  Total script run time: ', '%d:%02d:%02d' % (h, m, s)
