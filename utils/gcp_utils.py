from google.cloud import storage
from google.oauth2 import service_account
import json

with open("iucc-google-credentials.json", 'r') as f:
    creds = json.load(f)
credentials = service_account.Credentials.from_service_account_info(creds["google_auth"])

client = storage.Client(project=creds["google-storage"]["project_id"], credentials=credentials)

def read_data_from_cloud():
    bucket = client.bucket(creds["google-storage"]["bucket_name"])
    blob = bucket.blob("data.json")
    content = blob.download_as_text()
    json_data = json.loads(content)
    return json_data

def upload_data_to_cloud():
    bucket = client.bucket(creds["google-storage"]["bucket_name"])
    blob = bucket.blob("data.json")
    blob.upload_from_filename("data.json")

def remove_data_from_cloud():
    bucket = client.bucket(creds["google-storage"]["bucket_name"])
    blob = bucket.blob("data.json")
    blob.delete()