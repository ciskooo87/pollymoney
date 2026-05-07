from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Autonomous Prediction Market Trading Engine"
    app_env: str = "development"
    database_url: str
    redis_url: str
    polymarket_api_url: str
    polymarket_ws_url: str
    jwt_secret: str
    encryption_key: str
    enable_live_trading: bool = False
    require_human_approval: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
