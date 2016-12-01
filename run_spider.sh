#!/usr/bin/env bash

crawler=$1
city_id=$2
category_id=$3

scrapy crawl $crawler -a city_id=$city_id -a category_id=$category_id &

echo "Check the log file [dianping.log] for details"

exit 0
