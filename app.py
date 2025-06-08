from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import requests
from bs4 import BeautifulSoup
import uvicorn

app = FastAPI(
    title="Indian Railway Train Status API",
    description="API to get live train status from Indian Railway NTES",
    version="1.0.0"
)

class Station:
    def __init__(self):
        self.scheduled_arrival = None
        self.scheduled_departure = None
        self.actual_arrival = None
        self.actual_departure = None
        self.station_name = None
        self.station_code = None
        self.platform_number = None
        self.distance = None
    def __str__(self):
        return f"Station Name: {self.station_name}\nStation Code: {self.station_code}\nPlatform Number: {self.platform_number}\nDistance: {self.distance}\nScheduled Arrival: {self.scheduled_arrival}\nActual Arrival: {self.actual_arrival}\nScheduled Departure: {self.scheduled_departure}\nActual Departure: {self.actual_departure}"
    def to_dict(self):
        return {
            "station_name": self.station_name,
            "station_code": self.station_code,
            "platform_number": self.platform_number,
            "distance": self.distance,
            "scheduled_arrival": self.scheduled_arrival,
            "actual_arrival": self.actual_arrival,
            "scheduled_departure": self.scheduled_departure,
            "actual_departure": self.actual_departure
        }
    
class TrainDetails:
    def __init__(self):
        self.train_number = None
        self.train_name = None
        self.train_schedules = []
    def to_dict(self):
        return {
            "train_number": self.train_number,
            "train_name": self.train_name,
            "train_schedules": [schedule.to_dict() for schedule in self.train_schedules]
        }

class TrainSchedule:
    def __init__(self):
        self.train_date = None
        self.train_status = None
        self.train_station_details = []
    def to_dict(self):
        return {
            "train_date": self.train_date,
            "train_status": self.train_status,
            "train_station_details": [station.to_dict() for station in self.train_station_details]
        }
    

def station_details(station: Station):
    if "Yet to start from its source" in station.text:
        return "Yet to start from its source"
    station_object = Station()
    details = station.find_all("b")
    try:
        station_object.scheduled_arrival = details[0].text.strip()
        station_object.actual_arrival = details[1].text.strip()
        station_object.station_name = details[2].text.strip()
        if "PF" in details[3].text:
            station_object.station_code = details[3].text.split("  PF ")[0].strip()
            station_object.platform_number = details[3].text.split("  PF ")[1].strip().split("*")[0].strip()
        else:
            station_object.station_code = details[3].text.strip()
            station_object.platform_number = None
        if station_object.scheduled_arrival == "SRC":
            station_object.distance = "SRC"
            station_object.scheduled_departure = details[4].text.strip()
            station_object.actual_departure = details[5].text.strip()
        else:
            station_object.distance = details[4].text.strip() + " KMs"
            station_object.scheduled_departure = details[5].text.strip()
            station_object.actual_departure = details[6].text.strip()
    except:
        for i in details:
            print(i.text.strip())
        print("--------------------------------")

    return station_object

def train_details(train_number):
    "Date format: DD-MMM (08-Jun)"

    soup = BeautifulSoup(fetch_train_status(train_number), "html.parser")
    schedules = soup.find_all("div", {"id": "timeline-1"})

    train_details_object = TrainDetails()
    train_details_object.train_number = train_number
    train_details_object.train_name = soup.find_all("h5")[1].text.strip()

    for i in range(len(schedules)):
        schedule = schedules[i]
        train_schedule_object = TrainSchedule()
        first_station = station_details(schedule.find("div", {"class": "w3-card-2"}))
        if first_station == "Yet to start from its source":
            first_station = station_details(schedule.find_all("div", {"class": "w3-card-2"})[1])
        train_schedule_object.train_date = first_station.actual_departure.split(" ")[-1].upper()
        train_schedule_object.train_station_details = []
        for station in schedule.find_all("div", {"class": "w3-card-2"}):
            if "w3-sand" not in station.get("class"):
                train_schedule_object.train_station_details.append(station_details(station))
        train_schedule_object.train_status = soup.find_all("h6")[i].text.strip()
        train_details_object.train_schedules.append(train_schedule_object)
    
    return train_details_object
    

def fetch_train_status(train_number: str) -> str:
    """Fetch train status from Indian Railway website"""
    url = f"https://enquiry.indianrail.gov.in/mntes/tr?opt=TrainRunning&subOpt=FindRunningInstancePop&trainNo={train_number}&refDate="
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    form_data = f'lan=en&jFromStationInput=&jToStationInput=&trainType=XXX'
    
    files = {
        '_pd': (None, form_data)
    }
    
    try:
        response = requests.post(url, headers=headers, files=files, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch train status: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "Indian Railway Train Status API",
        "endpoints": {
            "GET /train/{train_number}": "Get train status by train number",
            "POST /train/status": "Get train status with custom parameters",
            "GET /docs": "API documentation"
        }
    }

@app.get("/train/{train_number}")
async def test_train_status(train_number: str):
    return train_details(train_number).to_dict()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)