#!/bin/bash

if [ -z "$sobi_access_token" ]
then
    (>&2 echo "Set env variable: \$sobi_access_token")
    exit 1
fi

url="https://app.socialbicycles.com/api/routes.json?access_token=$sobi_access_token"

curl -Ss "$url"
