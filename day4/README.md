# Docker anime bot

Pre-req:
1. Docker
2. Discord Bot Token, Guild Token, Channel Token

# Building Image

docker build .

# Running Container
docker run -itd --name bot --env-file ENV_FILE -v HOST_DEST:/anime_bot/file/ IMAGE

# ENV_FILE (sample)
DISCORD_TOKEN=

GUILD_TOKEN=

CHANNEL_TOKEN=

# Commands
!addanime URL_TO_GOGOANIME_ANIME
!watchlist
