from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(validation_alias="OPENAI_API_KEY")


_ = load_dotenv(find_dotenv())
if not _:
    _ = load_dotenv(".env")

local_settings = Settings()
