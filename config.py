from dataclasses import dataclass
from environs import Env

@dataclass
class Config:
    bot_token: str
    admin_ids: list[int]

@dataclass
class DatabaseConfig:
    database: str

@dataclass
class MainConfig:
    bot: Config
    db: DatabaseConfig

def load_config() -> MainConfig:
    env = Env()
    env.read_env()

    return MainConfig(
        bot=Config(
            bot_token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMIN_IDS")))
        ),
        db=DatabaseConfig(
            database=env.str("DATABASE_URL")
        )
    ) 