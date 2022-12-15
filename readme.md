
## local run rasa instance
rasa run --enable-api --cors="*"
rasa run actions


--endpoints.yml--
action_endpoint:
  url: "http://devtorium-bot-actions_server-1:5055/webhook"

## docker-compose
docker-compose
## 2 separate containers

docker network create rasa-bot-network
docker run  --net create rasa-bot-network --name action-server vadymkhomiyk/rasa-train:rasa-actions 
docker run -it -v C:\Users\Admin\train-bot:/app -p 5005:5005 --net create rasa-bot-network rasa/rasa:3.3.1-full shell


credentials.yml
add your webhook_url
ngrok http 5005
telegram:
  access_token: 5629623514:AAGyGlswxUCVbrvEzxbjCNKS19EudlNV5l4
  verify: d_train_bot
  webhook_url: --"https://11ac-178-74-235-30.eu.ngrok.io/webhooks/telegram/webhook"--


docker exec  -it train-bot-rasa_server-1 bash

http://localhost:5005/webhooks/rest/webhook
POST
{
	"sender": "test_user",
	"message": "radius Venus"
}