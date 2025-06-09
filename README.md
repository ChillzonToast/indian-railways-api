# Indian Railways API

A FastAPI-based REST API to get Indian Railways train information and live status.

## Features

- Get live train running status
- Get train schedule and station details
- Get trains between stations
- Clean JSON response format
- Built with FastAPI for high performance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/indian-railways-api.git
cd indian-railways-api
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
uvicorn app:app --reload
```

2. Access the API documentation:
- Open your browser and go to `http://localhost:8000/docs`
- Or use the ReDoc interface at `http://localhost:8000/redoc`

## API Endpoints

### Get Train Status
```http
GET /train/{train_number}
```
Get live status of a train by its number.

Example:
```bash
curl http://localhost:8000/train/12345
```

### Get Trains Between Stations
```http
GET /trains-between-stations/{from_station}/{to_station}
```
Get list of trains between two stations.

Example:
```bash
curl -X POST http://localhost:8000/trains/between-stations \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "from_station=BANGALORE CANT - BNC&to_station=KOLLAM JN - QLN&train_type=XXX"
```

## Response Format

### Train Status Response
```json
{
  "train_number": "16629",
  "train_name": "THIRUVANANTHAPURAM CENTRAL (TVC) - MANGALORE CENTRAL (MAQ)",
  "train_schedules": [
    {
      "train_date": "10-JUN*",
      "train_status": "Yet to start from its source",
      "train_station_details": [
        {
          "station_name": "THIRUVANANTHAPURAM CENTRAL",
          "station_code": "TVC",
          "platform_number": "4",
          "distance": "SRC",
          "scheduled_arrival": "SRC",
          "actual_arrival": "SRC",
          "scheduled_departure": "18:40 10-Jun",
          "actual_departure": "18:40 10-Jun*"
        },
        {
          "station_name": "KAZHAKUTTAM",
          "station_code": "KZK",
          "platform_number": "2",
          "distance": "13 KMs",
          "scheduled_arrival": "18:55 10-Jun",
          "actual_arrival": "18:55 10-Jun*",
          "scheduled_departure": "18:56 10-Jun",
          "actual_departure": "18:56 10-Jun*"
        },
        {
          "station_name": "MURUKKAMPUZHA",
          "station_code": "MQU",
          "platform_number": "1",
          "distance": "21 KMs",
          "scheduled_arrival": "19:06 10-Jun",
          "actual_arrival": "19:06 10-Jun*",
          "scheduled_departure": "19:07 10-Jun",
          "actual_departure": "19:07 10-Jun*"
        }
      ]
    }
  ]
}
```

### Trains Between Stations Response
```json
{
  "trains": [
    {
      "train_number": "16606",
      "train_name": "ERNAD EXPRESS",
      "from_station": "Thiruvananthapuram Central",
      "to_station": "Kozhikkode (Calicut)",
      "departure_time": "05.05",
      "arrival_time": "12.32",
      "duration": "07.27",
      "days": "1111111"
    },
    {
      "train_number": "16650",
      "train_name": "PARASURAM EXP",
      "from_station": "Kanniyakumari",
      "to_station": "Kozhikkode (Calicut)",
      "departure_time": "07.55",
      "arrival_time": "16.25",
      "duration": "08.30",
      "days": "1111111"
    }
  ]
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This API is not officially affiliated with Indian Railways. Use it at your own risk. The data is scraped from the official Indian Railways website and may not always be accurate or up-to-date.
