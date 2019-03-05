# sobi-save-to-strava

Tools to convert Social Bicycles (SoBi) rides into GPX, to upload to Strava

# Installation

1. Clone this repo

2. Install python dependencies

    ```
    pip install -r requirements.txt
    ```

3. Install [jq](https://stedolan.github.io/jq/)


# Usage

Set your SoBi access token:

```
export sobi_access_token="your access token here"
```

Download your most recent route:

```
./sobi-get-routes.sh | jq '.items[0]' > route.json
```

[Optionally] find the bike ID

```
bike_id=$(jq '.bike_id' route.json)
```

[Optionally] use that bike ID to look up its "name" in the system:

```
./sobi-get-bike.sh "$bike_id" | jq -r '.name'
```

Convert SoBi's route JSON into GPX:

```
./sobi_route_to_gpx.py route.json > route.gpx
```

That `route.gpx` file should be good to manually upload to Strava, here:

- https://www.strava.com/upload/select


# TODO

Use Strava's API to auto-upload activities

https://developers.strava.com/docs/uploads/

# Other Resources

- https://app.socialbicycles.com/developer
- https://github.com/tkrajina/gpxpy
- https://en.wikipedia.org/wiki/GPS_Exchange_Format
- https://github.com/newvem/pytz
