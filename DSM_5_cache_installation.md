# DSM 5 cache installation

> It is necessary to create an image `redis:7-alpine` for the required architecture, for example through Scopeo and install it into docker

Connect to your dsm via `ssh`

```bash
# create target dir
mkdir -m cache/data

cd cache

# copy redis dump into data if it exists

# copy redis conf into .

docker run -d \
  --name AudioTagLoader \
  --restart always \
  -p 6379:6379 \
  -v /volume1/docker/Containers/AudioTagLoader/data:/data \
  -v /volume1/docker/Containers/AudioTagLoader/redis.conf:/redis.conf \
  redis:7-alpine \
  redis-server /redis.conf --requirepass REDIS_PASSWORD

# change "/volume1/docker/Containers/AudioTagLoader" to your path to cache
```

