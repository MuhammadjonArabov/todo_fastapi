from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    db_username: str
    db_password: str

    class Config:
        env_file = ".env"


settings = Settings()
