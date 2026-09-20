from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
class AgentSettings(BaseSettings):
    model_config=SettingsConfigDict(env_prefix="TELEMETRY_",env_file=".env",extra="ignore")
    data_dir:Path=Field(default=Path.home()/".endpoint_telemetry")
    server_url:str="http://127.0.0.1:8000"
    device_id:str=""
    enrollment_token:str=""
    enabled_categories:str="system,hardware,storage,applications,browsers,network,power"
    @property
    def categories(self): return [x.strip() for x in self.enabled_categories.split(",") if x.strip()]
    def ensure_data_dir(self): self.data_dir.mkdir(parents=True,exist_ok=True)
