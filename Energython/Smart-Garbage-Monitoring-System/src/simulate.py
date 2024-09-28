import firebase_admin
from firebase_admin import credentials, db
import random
import time

# Initialize Firebase
def initialize_firebase():
    cred = credentials.Certificate("data/firebase_credentials/waste-management-ec581-firebase-adminsdk-x5b5i-aa18930a36.json")

    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://waste-management-ec581-default-rtdb.firebaseio.com/'
    })

# Function to simulate garbage bin distance data
def simulate_data(bin_id, min_distance=0, max_distance=200):
    distance = random.randint(min_distance, max_distance)
    return distance

# Push simulated data to Firebase
def push_data_to_firebase(bin_id, distance):
    ref = db.reference(f"/{bin_id}/state")  # Adjusted path to match expected structure
    ref.set({'state': distance})

if __name__ == "__main__":
    initialize_firebase()

    bins = [101, 102, 103, 104, 105]  # List of bin IDs
    update_interval = 10  # Time in seconds

    while True:
        for bin_id in bins:
            distance = simulate_data(bin_id)
            push_data_to_firebase(bin_id, distance)
            print(f"Simulated and updated bin {bin_id} with distance {distance}cm.")
        
        time.sleep(update_interval)
