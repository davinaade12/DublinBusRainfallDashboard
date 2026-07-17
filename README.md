# Dublin Bus Rainfall Dashboard

## Overview

The Dublin Bus Rainfall Dashboard is a web-based analytics application developed as part of a third-year Data Science Academic Internship module at the National College of Ireland.

The application investigates whether rainfall affects Dublin Bus punctuality by combining live weather data from Met Éireann with live GTFS-Realtime bus information from the National Transport Authority (NTA). Historical observations are stored in Firebase Firestore, allowing users to analyse trends and relationships over time.

---

## Features

- Live Dublin Bus GTFS-Realtime data
- Live Met Éireann weather data
- Dashboard displaying key performance indicators
- Historical analytics dashboard
- Rainfall and delay trend charts
- Rainfall vs delay scatter plot
- Pearson correlation analysis
- Automatic snapshot collection
- Firebase Firestore cloud storage
- CSV export
- Responsive Bootstrap interface

---

## Technologies Used

### Backend

- Python
- Flask
- Firebase Admin SDK
- Requests

### Frontend

- HTML
- Bootstrap 5
- JavaScript
- Chart.js

### Database

- Firebase Firestore

### Testing

- Pytest

### Version Control

- Git
- GitHub

---

## APIs Used

### Met Éireann

Provides live rainfall information used for weather analysis.

### National Transport Authority (GTFS-Realtime)

Provides live Dublin Bus trip updates and delay information.

---

## Project Structure

```
DublinBusRainfallDashboard
│
├── app.py
├── config.py
├── routes/
├── services/
├── templates/
├── static/
├── data/
├── firebase/
├── tests/
└── requirements.txt
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/davinaade12/DublinBusRainfallDashboard.git
```

Navigate into the project

```bash
cd DublinBusRainfallDashboard
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open the browser

```
http://127.0.0.1:5000
```

---

## Testing

Run the automated tests using:

```bash
python -m pytest
```

---

## Future Improvements

- Longer-term historical data collection
- Additional Dublin Bus routes
- More weather variables (wind, temperature)
- Predictive machine learning model for bus delays
- Interactive dashboard filters

---

## Author

Davina Adegboyega

BSc (Hons) Data Science

National College of Ireland

2026