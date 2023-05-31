import base64
from enum import Enum

from fastapi import FastAPI
from fastapi.responses import Response

from src.libraries.image import image_to_base64
from src.libraries.maimai_best_40 import generate
from src.libraries.maimai_best_50 import generate50

app = FastAPI()


class B450Enum(str, Enum):
    b40 = 'b40'
    b50 = 'b50'


@app.get("/{b450}/{username}")
async def b450(b450: B450Enum, username: str):
    #
    payload = {'username': username}

    if b450.b50 == 'b50':
        payload['b50'] = True

    generate_func = generate \
        if b450 is B450Enum.b40 \
        else generate50

    img, success = await generate_func(payload)

    if success != 0:
        # https://www.reddit.com/r/ProgrammerHumor/comments/q4g93s/why/
        return {'status': success}

    # https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi
    image_bytes: bytes = base64.b64decode(image_to_base64(img))
    return Response(content=image_bytes, media_type="image/png")
