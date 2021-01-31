# optimal-route-ga

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Example](#example)

## General info
Python implementation of genetic algo to find optimal route across different destinations.
if just name locations are passed, google api is used to find the distances of all A to B combinations

## Setup
activate your virtualenv
```
pip install -r requirements.txt
```
## Example
```python
from src.optimal_route_ga import OptimalRoute

GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
my_waypoints = ["Thessaloniki, Greece",
                 "Grevena, Greece",
                 "Olympos, Greece",
                 "Kalampaka, Greece",
                 "Metsovo, Greece",
                 "Katerini, Greece",
                 "Trikala, Greece",
                 "kilkis, Greece",
                 "kozani, Greece",
                 "Salamina, Greece"]
          
OptimalRoute_Thessaloniki_Salamina = OptimalRoute(waypoints_lst = my_waypoints, api_key=GOOGLE_API_KEY, verbose=False)
optimal_route = OptimalRoute_Thessaloniki_Salamina.run_genetic_algorithm()
print(optimal_route)
```

