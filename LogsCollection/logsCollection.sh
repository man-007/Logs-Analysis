#!/bin/bash

currentTime=0
namespace=$1
microservice=$2
currentDirectoryPath=$3
terminationTime=$4
collectionInterval=$5
logFile="$microservice"Logs
date=$(date '+%d_%m_%Y_%H:%M:%S')
dateDiff=$(date +%s)
while (( currentTime < terminationTime ));
do
        date=$(date '+%d_%m_%Y_%H:%M:%S') # to store it in particular file according to name
        dateDiff=$(date +%s) # to calculate the time difference
        kubectl get po -n $namespace |grep $microservice | awk '{print $1}' | xargs kubectl logs -n $namespace > "$currentDirectoryPath"/"$microservice"Logs_"$date".txt

        timeFinished=$(($(date +%s)-dateDiff))
        printf "sleeping for %s seconds" "$timeFinished"
        sleep $((collectionInterval-timeFinished))
        currentTime=$((currentTime+$collectionInterval))
        echo $currentTime
done
echo "Done!"
