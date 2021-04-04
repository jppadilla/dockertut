FROM python:slim
SHELL ["/bin/bash", "-c"]
ENV ANIME_DIRECTORY=${HOME}/anime_bot/
WORKDIR ${ANIME_DIRECTORY}
COPY anime_bot/* .
RUN pip3 install -r requirements.txt
VOLUME [ "${ANIME_DIRECTORY}/file/" ]
ENTRYPOINT [ "python3" ] 
CMD [ "anime_bot.py" ]
