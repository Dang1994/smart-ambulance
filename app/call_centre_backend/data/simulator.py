from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# Predefined lists to generate random case data
case_types = ["Accident", "Medical", "Fire", "Delivery", "Trauma"]
caller_names = ["Narendra Kheti", "Bikram Adabar", "Suresh Patra", "Deepak Meher", "Ravi Sahu"]
locations = ["Atabira Near College, City A", "Budharaja, Sambalpur", "Puri Beach", "Bargarh Market", "Baripada Station"]
contacts = ["9178665036", "6370576743", "7896541230", "8765432190", "9123456780"]

# Simulate random GPS coordinates (lat, long)
def generate_random_gps():
    latitude = round(random.uniform(20.0, 22.0), 6)  # Odisha latitude range for simulation
    longitude = round(random.uniform(83.0, 86.0), 6)  # Odisha longitude range for simulation
    return f"{latitude}, {longitude}"

# Function to generate a random emergency case with GPS or manual location
def generate_random_case():
    use_gps = random.choice([True, False])  # Randomly choose between GPS and manual location
    case_data = {
        "caseNumber": f"CASE{random.randint(100, 999)}",  # Generate random case number
        "emergencyType": random.choice(case_types),
        "numInjured": random.randint(1, 5),  # Random number of injured individuals
        "callerName": random.choice(caller_names),
        "callerContact": random.choice(contacts),
        "location": generate_random_gps() if use_gps else random.choice(locations),  # GPS or manual location
        "ambulanceStatus": "Pending",
        "eta": "Unknown",  # ETA will be updated later
        "approved": False
    }
    
    # Add a random delay to simulate the emergency approval process and ambulance dispatch
    if random.choice([True, False]):
        case_data["approved"] = True
        case_data["ambulanceStatus"] = "Dispatched"
        case_data["eta"] = f"{random.randint(5, 20)} minutes"
    
    return case_data

# API endpoint to fetch new cases
@app.route('/cases', methods=['GET'])
def get_cases():
    # Simulate delay to represent real-time case arrival
    time.sleep(1)  # Simulate a small delay (optional)
    
    new_case = generate_random_case()  # Generate random case
    return jsonify([new_case])  # Return the case as a list

if __name__ == '__main__':
    app.run(debug=True)
