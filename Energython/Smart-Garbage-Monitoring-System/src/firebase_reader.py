import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class FirebaseReader:
    def __init__(self):
        cred = credentials.Certificate("data/firebase_credentials/waste-management-ec581-firebase-adminsdk-x5b5i-0b30bccf29.json")

        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://waste-management-ec581-default-rtdb.firebaseio.com/'
        })

        self.ref = db.reference('/')

    def get_active_bins(self):
        active_bins = []
        data = self.ref.get()

        for node in data:
            # Access the nested 'state' key
            if 'state' in data[node] and 'state' in data[node]['state'] and data[node]['state']['state'] < 50:
                active_bins.append(node)

        return active_bins