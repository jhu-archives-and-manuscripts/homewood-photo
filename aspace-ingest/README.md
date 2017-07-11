Order of operations:

1. Create missing agents from agents csv using postAgents.py.
2. Identify uri of resource record and uri of container_profile for collection (creating a container_profile if one does not exist).  Post top_containers from top_containers csv using postContainersFromCSV.py, supplying uri's when requested.
3. Confirm file format type of "dng" exists in file format types controlled value list.  Post digital_objects from digital_objects csv using postDOs.py.
4. Modify master archival_object spreadsheet to include new agents, top_container, and digital_object uris.
5. Identify uri of resource record and uri of parent series record.  Post archival_objects using postAOs.py.
