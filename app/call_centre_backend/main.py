from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from data.cases import cases
from data.ambulances import ambulances
from data.hospitals import hospitals

app = FastAPI()

# Root Route
@app.get("/")
def read_root():
    return {"message": "Welcome to the SG Ambulance Backend API"}

# Get all emergency cases
@app.get("/cases")
def get_cases():
    return cases

# Approve a case
@app.put("/cases/{case_id}/approve")
def approve_case(case_id: int):
    for case in cases:
        if case["id"] == case_id:
            case["approved"] = True
            return {"message": f"Case {case['caseNumber']} approved", "case": case}
    raise HTTPException(status_code=404, detail="Case not found")

# Dispatch an ambulance to a case
@app.put("/cases/{case_id}/dispatch")
def dispatch_ambulance(case_id: int):
    for case in cases:
        if case["id"] == case_id and case["approved"]:
            for ambulance in ambulances:
                if ambulance["availability"]:
                    ambulance["status"] = "Dispatched"
                    ambulance["availability"] = False
                    case["ambulanceStatus"] = "Dispatched"
                    case["eta"] = "10 minutes"
                    return {"message": f"Ambulance dispatched to case {case['caseNumber']}", "ambulance": ambulance}
            return {"message": "No available ambulances"}
    raise HTTPException(status_code=400, detail="Case not approved or not found")

# Add CORS middleware to allow your React frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL (e.g., "http://localhost:3000")
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get all ambulances
@app.get("/ambulances")
def get_ambulances():
    return ambulances

# Get all hospitals
@app.get("/hospitals")
def get_hospitals():
    return hospitals

# Example route
@app.get("/cases")
def get_cases():
    return cases
