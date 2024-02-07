#!/bin/bash

docker build -t reminder -f ./reminder/worker/question_generation/Dockerfile .
docker tag reminder:latest 844790362879.dkr.ecr.ap-northeast-1.amazonaws.com/reminder:latest
docker push 844790362879.dkr.ecr.ap-northeast-1.amazonaws.com/reminder:latest