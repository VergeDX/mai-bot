FROM busybox AS src_static
ADD https://www.diving-fish.com/maibot/static.zip .
RUN unzip static.zip

FROM alpine AS base
RUN apk add python3 py3-pip

FROM base as mb_base
RUN pip install fastapi uvicorn && \
    pip install aiohttp pillow requests

# https://docs.docker.com/get-started/02_our_app/

FROM mb_base
WORKDIR /mai-bot
COPY . .
COPY --from=src_static src/static src/static
CMD ["python", "b450.py"]
