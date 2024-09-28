import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--town_name', type=str, default="pondicherry_india")
    
    name = parser.parse_args().town_name
    cred = credentials.Certificate("data/firebase_credentials/data/firebase_credentials/waste-management-ec581-firebase-adminsdk-x5b5i-aa18930a36.json")

    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://waste-management-ec581-default-rtdb.firebaseio.com/'
    })

    ref = db.reference("/")

    with open(f'data/maps/{name}/{name}_bin_data.json', "r") as file:
        bin_data = json.load(file)

    ref.set(bin_data)
 
if __name__ == "__main__":
    main()