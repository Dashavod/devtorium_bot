
## local run rasa instance
rasa run --enable-api --cors="*"
rasa run actions


--endpoints.yml--
action_endpoint:
  url: "http://train-bot-actions_server-1:5055/webhook"

## docker-compose
docker-compose
## 2 separate containers

docker network create rasa-bot-network
docker run  --net create rasa-bot-network --name action-server vadymkhomiyk/rasa-train:rasa-actions 
docker run -it -v C:\Users\Admin\train-bot:/app -p 5005:5005 --net create rasa-bot-network rasa/rasa:3.3.1-full shell


endpoints.yml

action_endpoint:
  url: "http://name-actions-container:5055/webhook"


docker exec  -it train-bot-rasa_server-1 bash