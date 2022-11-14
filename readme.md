rasa run --enable-api --cors="*"
rasa run actions



docker run  --net my-project --name action-server vadymkhomiyk/rasa-train:rasa-actions 
docker run -it -v C:\Users\Admin\train-bot:/app -p 5005:5005 --net my-project rasa/rasa:3.3.1-full shell

docker-compose exec rasa bash