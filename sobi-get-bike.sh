#!/bin/bash

# Sample data:
# {
#   "id": 10863,
#   "name": "2649",
#   "network_id": 31,
#   "sponsored": false,
#   "hub_id": 2168,
#   "inside_area": true,
#   "address": "40-68 Andrew Young International Boulevard Northwest, Atlanta",
#   "current_position": {
#     "type": "Point",
#     "coordinates": [
#       -84.38934333333333,
#       33.75971166666667
#     ]
#   },
#   "bonuses": []
# }

if [ -z "$sobi_access_token" ]
then
    (>&2 echo "Set env variable: \$sobi_access_token") ;
    exit 1 ;
fi

bike_id="$1"

if [ -z "$bike_id" ]
then
    (>&2 echo "Missing bike id") ;
    exit 1 ;
fi


url="https://app.socialbicycles.com/api/bikes/$bike_id.json?access_token=$sobi_access_token" ;

curl -Ss "$url" ;
