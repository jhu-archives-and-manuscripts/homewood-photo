Order of operations:

1. Create missing agents from agents csv using postAgents.py.
2. Post top_containers from top_containers csv using postContainersFromCSV.py.
3. Post digital_objects from digital_objects csv using postDOs.py.
4. From within ArchivesSpace staff interface create series under which all archival_objects will exist.  Note the uri for this parent series (you will be prompted to enter it when running the postAOs.py script).
5. Modify master archival_object spreadsheet to include new agent, top_container, and digital_object uris.
6. Post archival_objects using postAOs.py.
