from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    BOT_API: str
    HOST: str
    PORT: str
    URL: str

    class Config():
        env_file = '.env'

bot_settings = Settings()
