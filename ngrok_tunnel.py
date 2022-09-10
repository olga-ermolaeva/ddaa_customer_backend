import os
import io
import sys
import glob

from fastapi.logger import logger
from pydantic import BaseSettings


# ngrox
class Settings(BaseSettings):
    # ... The rest of our FastAPI settings

    BASE_URL = "http://localhost:8000"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"


settings = Settings()


def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass


#webhooks
#if settings.USE_NGROK:
#if True:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
from pyngrok import ngrok

ngrok.set_auth_token("2EaiDnEErgs0tmcWGXz351gFAnV_5JM2UPBbWdjFBLYbCVFY9")
    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000

    # Open a ngrok tunnel to the dev server
public_url = ngrok.connect(port).public_url
logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL
settings.BASE_URL = public_url
#init_webhooks(public_url)