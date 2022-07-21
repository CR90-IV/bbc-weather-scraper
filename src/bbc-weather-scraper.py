import pandas as pd
from datetime import datetime
from apiwrapper import RestConsumer
bbc_weather = RestConsumer(base_url="https://weather-broker-cdn.api.bbci.co.uk/en/", append_slash=True)

locations = {
    "2643743" : "Greater London",
    "2634341" : "City of Westminster",
    "2650225" : "Edinburgh",
    "2653822" : "Cardiff",
    "2655984" : "Belfast",
    "2988507" : "Paris",
    "4140963" : "Washington DC",
    "105343"  : "Jeddah",
    "2147714" : "Sydney"
    }

def append_location_details(df, location_id, location_name):
    df['location_id'] = location_id
    df['location_name'] = location_name
    return df

def save_scrape_to_csv(df, folder, label):
    time_now_string = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = "{}/scrape_{}_{}.csv".format(folder, label.replace(" ",""), time_now_string)
    df.to_csv(filepath, index=False)

for location_id, location_name in locations.items():
    response = bbc_weather.forecast.aggregated[location_id]()
    print(response) # for debugging
    results = pd.DataFrame.from_records(response["forecasts"])

    # Detailed forecasts
    detailed = pd.json_normalize(results["detailed"], ["reports"], ["issueDate", "lastUpdated"])
    detailed = append_location_details(detailed, location_id, location_name)
    save_scrape_to_csv(detailed, "output/scrapes/detailed", label=location_name)

    # Daily summaries
    summary = pd.json_normalize(results["summary"])
    summary = append_location_details(summary, location_id, location_name)
    save_scrape_to_csv(summary, "output/scrapes/summary", label=location_name)



