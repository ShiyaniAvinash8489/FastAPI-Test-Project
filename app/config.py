# Import Settings
from pydantic import BaseSettings


"""
****************************************************************************************
                                    Setting For Hiding Key 
****************************************************************************************
"""


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    email_username: str
    email_password: str
    smtp_server: str
    smtp_port: int
    twilio_sid: str
    twilio_auth_token: str
    twilio_service_id: str
    google_client_id: str
    google_client_secret: str
    google_password: str

    class Config:
        env_file = ".env"


settings = Settings()
