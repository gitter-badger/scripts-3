#!/bin/bash

MESSAGE=$1

DATA="
  {\"msgtype\": \"text\",
    \"text\": {
        \"content\":\"$MESSAGE\"
     }
  } 
"

echo $DATA

curl 'https://oapi.dingtalk.com/robot/send?access_token=50a1ea887baef8719c27adb38fbc48c883f487c0d5d18966007b802c92085d04' \
   -H 'Content-Type: application/json' \
   -d "$DATA"
