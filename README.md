# optimal-route-ga

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Example](#example)

## General info
Python implementation of genetic algo to find optimal route
Algo to calculate optimal route across different locations.
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
all_waypoints = ["Kalamaria, Greece",
                 "Grevena, Greece",
                 "Olympos, Greece",
                 "Kalampaka, Greece",
                 "Metsovo, Greece",
                 "Katerini, Greece",
                 "Trikala, Greece",
                 "kilkis, Greece",
                 "kozani, Greece",
                 "Salamina, Greece"]
          
OptimalRoute_kalamaria_milan = OptimalRoute(waypoint_combinations_distance_df=None,waypoints_lst = all_waypoints,api_key=GOOGLE_API_KEY,verbose=False)
optimal_route = OptimalRoute_kalamaria_milan.run_genetic_algorithm()
print(optimal_route)
```

