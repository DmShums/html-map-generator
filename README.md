# html-map-generator

Here is located python script to generate html page with map.
It generates 10 closest film location of a given year

## Run file by using this command
```python
python3 main.py 2000 49.83826 24.02324 path_to_dataset
```

## Libraries used here
```python
from math import radians, cos, sin, asin, sqrt
import argparse
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut
```

## To avoid run time error make 'location.list' file shorter
## Example of a map:

![](https://drive.google.com/uc?export=view&amp;id=1gwK0pcaqG0GY6ixyNfveg3zW0_UmStn0)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
