#!/bin/bash
total_time=0
url="http://localhost:8000/api/v1/transactions"
for i in {1..10}; do
    response=$(curl -s -o /dev/null -w "%{http_code} %{time_total}\n" "$url")
    response_time=$(echo "$response" | cut -d " " -f 2)
    total_time=$(echo "$total_time + $response_time" | bc)
done
average_time=$(echo "scale=3; $total_time / 10" | bc)
echo "Average response time: ${average_time}s at ${url}"