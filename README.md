# optimal-route-ga

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Demo](#demo)

## General info
Python implementation of genetic algo to find optimal route across different destinations.
if just name locations are passed, google api is used to find the distances of all A to B combinations

## Setup
activate your virtualenv
```
pip install -r requirements.txt
```
## Demo
```python
from src.optimal_route_ga import OptimalRoute

GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
london_attractions = ["Big Ben, London", 
                      "Hyde Park, London",
                      "Westminster Abbey, London",
                      "London Eye",
                      "Tower of London",
                      "Piccadilly Circus",
                      "Buckingham Palace, London",
                      "National Gallery, London",
                      "Trafalgar Square, London"
                     ]
          
OptimalRoute_london_attractions = OptimalRoute(waypoint_combinations_distance_df=None,waypoints_lst = london_attractions,api_key=GOOGLE_API_KEY,verbose=False)
optimal_route_london_attractions = OptimalRoute_london_attractions.run_genetic_algorithm()
print(optimal_route_london_attractions)

OptimalRoute_london_attractions.draw_optimal_route_map()
OptimalRoute_london_attractions.display_optimal_route_map()

```
![demo img](https://github.com/kostasvog1/optimal-route-ga/blob/main/plots/optimal_route_ga_demo_img1.PNG?raw=true)

