#!/bin/bash

python redis_cache.py &

python main.py &

wait