set -e
rm -rf ./db/dev_data
rm -rf ./db/dev_redis
DATABASE_LOCATION="./db/dev_data" REDIS_LOCATION="./db/dev_redis" docker compose up powermemo-server-db powermemo-server-redis
rm -rf ./db/dev_data
rm -rf ./db/dev_redis