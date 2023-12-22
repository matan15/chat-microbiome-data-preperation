import os
from tkinter.messagebox import showwarning, askyesno
from tkinter import simpledialog
import json


def setup_config():
    if "iucc-google-credentials.json" not in os.listdir():
        showwarning("No credentials found", "There are no credentials or some credentials are missing, after you will click 'ok', fill the fields to setup the credentials.")
        creds = {
            "google-storage": {
                "project_id": "",
                "bucket_name": ""
            },
            "google_auth": {
                "type": "",
                "project_id": "",
                "private_key_id": "",
                "private_key": "",
                "client_email": "",
                "client_id": "",
                "auth_uri": "",
                "token_uri": "",
                "auth_provider_x509_cert_url": "",
                "client_x509_cert_url": "",
                "universe_domain": ""
            }
        }

        project_id = simpledialog.askstring("Configure Credentials", "Enter the project id:")
        while not project_id:
            answer = askyesno("Not valid value", "You have been entered a not valid value, do you want to enter a new value (yes) or exit (no)?")
            if answer:
                project_id = simpledialog.askstring("Configure Credentials", "Enter the project id:")
            else:
                return False
            
        creds["google-storage"]["project_id"] = project_id
        creds["google_auth"]["project_id"] = project_id

        bucket_name = simpledialog.askstring("Configure Credentials", "Enter the bucket name:")
        while not bucket_name:
            answer = askyesno("Not valid value", "You have been entered a not valid value, do you want to enter a new value (yes) or exit (no)?")
            if answer:
                bucket_name = simpledialog.askstring("Configure Credentials", "Enter the bucket name:")
            else:
                return False
            
        creds["google-storage"]["bucket_name"] = bucket_name

        type = simpledialog.askstring("Configure Credentials", "Enter the type in google auth:")
        while not type:
            answer = askyesno("Not valid value", "You have been entered a not valid value, do you want to enter a new value (yes) or exit (no)?")
            if answer:
                type = simpledialog.askstring("Configure Credentials", "Enter the type in google auth:")
            else:
                return False
        
        creds["google_auth"]["type"] = type

        private_key_id = simpledialog.askstring("Configure Credentials", "Enter the private key id:")
        while not private_key_id:
            answer = askyesno("Not valid value", "You have been entered a not valid value, do you want to enter a new value (yes) or exit (no)?")
            if answer:
                private_key_id = simpledialog.askstring("Configure Credentials", "Enter the private key id:")
            else:
                return False
            
        creds["google_auth"]["private_key_id"] = private_key_id

        private_key = simpledialog.askstring("Configure Credentials", "Enter the private key:")
        while not private_key:
            answer = askyesno("Not valid value", "You have been entered a not valid value, do you want to enter a new value (yes) or exit (no)?")
            if answer:
                private_key = simpledialog.askstring("Configure Credentials", "Enter the private key:")
            else:
                return False
        
        creds["google_auth"]["private_key"] = private_key.replace("\\n", "\n")

        client_email = simpledialog.askstring("Configure Credentials", "Enter the cleint email:")
        while not client_email:
            answer = askyesno("Not valid value", "You have been entered a not valid value, do you want to enter a new value (yes) or exit (no)?")
            if answer:
                client_email = simpledialog.askstring("Configure Credentials", "Enter the cleint email:")
            else:
                return False
            
        creds["google_auth"]["client_email"] = client_email

        client_id = simpledialog.askstring("Configure Credentials", "Enter the client id:")
        while not client_id:
            answer = askyesno("Not valid value", "You have been entered a not valid value, do you want to enter a new value (yes) or exit (no)?")
            if answer:
                client_id = simpledialog.askstring("Configure Credentials", "Enter the client id:")
            else:
                return False
            
        creds["google_auth"]["client_id"] = client_id

        auth_uri = simpledialog.askstring("Configure Credentials", "Enter the auth uri:")
        while not auth_uri:
            answer = askyesno("Not valid value", "You have been entered a not valid value, do you want to enter a new value (yes) or exit (no)?")
            if answer:
                auth_uri = simpledialog.askstring("Configure Credentials", "Enter the auth uri:")
            else:
                return False
            
        creds["google_auth"]["auth_uri"] = auth_uri

        token_uri = simpledialog.askstring("Configure Credentials", "Enter the token uri:")
        while not token_uri:
            answer = askyesno("Not valid value", "You have been entered a not valid value, do you want to enter a new value (yes) or exit (no)?")
            if answer:
                token_uri = simpledialog.askstring("Configure Credentials", "Enter the token uri:")
            else:
                return False
        
        creds["google_auth"]["token_uri"] = token_uri

        auth_provider_x509_cert_url = simpledialog.askstring("Configure Credentials", "Enter the auth provider x509 cert url:")
        while not auth_provider_x509_cert_url:
            answer = askyesno("Not valid value", "You have been entered a not valid value, do you want to enter a new value (yes) or exit (no)?")
            if answer:
                auth_provider_x509_cert_url = simpledialog.askstring("Configure Credentials", "Enter the auth provider x509 cert url:")
            else:
                return False
            
        creds["google_auth"]["auth_provider_x509_cert_url"] = auth_provider_x509_cert_url

        client_x509_cert_url = simpledialog.askstring("Configure Credentials", "Enter the client x509 cert url:")
        while not client_x509_cert_url:
            answer = askyesno("Not valid value", "You have been entered a not valid value, do you want to enter a new value (yes) or exit (no)?")
            if answer:
                client_x509_cert_url = simpledialog.askstring("Configure Credentials", "Enter the client x509 cert url:")
            else:
                return False
            
        creds["google_auth"]["client_x509_cert_url"] = client_x509_cert_url

        universe_domain = simpledialog.askstring("Configure Credentials", "Enter the universe domain:")
        while not universe_domain:
            answer = askyesno("Not valid value", "You have been entered a not valid value, do you want to enter a new value (yes) or exit (no)?")
            if answer:
                universe_domain = simpledialog.askstring("Configure Credentials", "Enter the universe domain:")
            else:
                return False
            
        creds["google_auth"]["universe_domain"] = universe_domain

        with open("iucc-google-credentials.json", 'w') as f:
            json.dump(creds, f)
        
    return True