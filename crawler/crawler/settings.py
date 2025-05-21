from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


SETTINGS_CONFIG = SettingsConfigDict(
    env_file=".env",
    extra="ignore",
    protected_namespaces=("settings_",)
)


class ScrapySettings(BaseSettings):
    model_config = SETTINGS_CONFIG
    bot_name: Optional[str] = Field(
        default="search-engine-crawler", alias="BOT_NAME"
    )
    log_level: Optional[str] = Field(
        default="INFO", alias="LOG_LEVEL"
    )
    spider_modules: Optional[list[str]] = Field(
        default=["crawler.spiders"], alias="SPIDER_MODULES"
    )
    newspider_module: Optional[str] = Field(
        default="crawler.spiders", alias="NEWSPIDER_MODULE"
    )
    robotstxt_obey: Optional[bool] = Field(
        default=True, alias="ROBOTSTXT_OBEY"
    )
    item_pipelines: Optional[dict[str, int]] = Field(
        default={"crawler.pipelines.IndexPipeline": 300}, alias="ITEM_PIPELINES"
    )
    max_idle_time_before_close: Optional[int] = Field(
        default=30, alias="MAX_IDLE_TIME_BEFORE_CLOSE"
    )
    scheduler: Optional[str] = Field(
        default="scrapy_redis.scheduler.Scheduler", alias="SCHEDULER"
    )
    scheduler_persist: Optional[bool] = Field(
        default=True, alias="SCHEDULER_PERSIST"
    )
    dupefilter_class: Optional[str] = Field(
        default="scrapy_redis.dupefilter.RFPDupeFilter", alias="DUPEFILTER_CLASS"
    )
    redis_url: Optional[str] = Field(
        default=None, alias="REDIS_URL"
    )
    request_fingerprinter_implementation: Optional[str] = Field(
        default="2.7", alias="REQUEST_FINGERPRINTER_IMPLEMENTATION"
    )
    twisted_reactor: Optional[str] = Field(
        default="twisted.internet.asyncioreactor.AsyncioSelectorReactor", alias="TWISTED_REACTOR"
    )
    feed_export_encoding: Optional[str] = Field(
        default="utf-8", alias="FEED_EXPORT_ENCODING"
    )

    def env_values(self) -> dict[str, any]:
        return {field.upper(): getattr(self, field) for field in self.model_fields}


class EmbeddingSettings(BaseSettings):
    model_config = SETTINGS_CONFIG
    model_name: Optional[str] = Field(
        default="jinaai/jina-embeddings-v3", alias="EMBEDDING_MODEL_NAME"
    )
    token_to_word_ratio: Optional[float] = Field(
        default=0.75, alias="EMBEDDING_TOKEN_TO_WORD_RATIO"
    )
    supported_languages: Optional[set[str]] = Field(
        default={"en", "uk"}, alias="EMBEDDING_SUPPORTED_LANGUAGES"
    )


class MongoSettings(BaseSettings):
    model_config = SETTINGS_CONFIG
    db_name: Optional[str] = Field(
        default="search-engine", alias="MONGO_DB_NAME"
    )
    url: Optional[str] = Field(
        default=None, alias="MONGO_URL"
    )


class Settings(BaseSettings):
    model_config = SETTINGS_CONFIG
    scrapy: Optional[ScrapySettings] = Field(
        default=ScrapySettings()
    )
    embedding: Optional[EmbeddingSettings] = Field(
        default=EmbeddingSettings()
    )
    mongo: Optional[MongoSettings] = Field(
        default=MongoSettings()
    )


locals().update(Settings().scrapy.env_values())
