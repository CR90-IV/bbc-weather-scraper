import pandas as pd
from datetime import datetime
from apiwrapper import RestConsumer
bbc_weather = RestConsumer(base_url="https://weather-broker-cdn.api.bbci.co.uk/en/", append_slash=True)

locations = ["2643743"]

for location in locations:
    response = bbc_weather.forecast.aggregated[location]()

    detailed = pd.json_normalize(response["forecasts"], ["detailed", "reports"], meta=[["detailed", "issueDate"], ["detailed", "lastUpdated"]])
    detailed['location'] = "2643743"


    # Save as CSV
    time_now_string = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    results.to_csv("output/scrapes/detailed/scrape_{}_{}.csv".format(location, time_now_string), index=False)


