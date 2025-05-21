from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


SETTINGS_CONFIG = SettingsConfigDict(
    env_file=".env",
    extra="ignore"
)


class EmbeddingSettings(BaseSettings):
    model_config = SETTINGS_CONFIG
    model_name: Optional[str] = Field(
        default="jinaai/jina-embeddings-v3", alias="EMBEDDING_MODEL_NAME"
    )


class MongoSettings(BaseSettings):
    model_config = SETTINGS_CONFIG
    db_name: Optional[str] = Field(
        default="search-engine", alias="MONGO_DB_NAME"
    )
    url: Optional[str] = Field(
        default=None, alias="MONGO_URL"
    )


class CohereSettings(BaseSettings):
    model_config = SETTINGS_CONFIG
    api_key: Optional[str] = Field(
        default=None, alias="COHERE_API_KEY"
    )
    model_name: Optional[str] = Field(
        default="command-a-03-2025", alias="COHERE_MODEL_NAME"
    )
    system_prompt: Optional[str] = Field(
        default=(
            "You are a sophisticated multilingual search engine designed to respond to queries in the user's language. "
            "Your role is to scour a range of documents, selecting those that align with the semantic intent of the "
            "query. You should prioritize results that match both the language and the meaning of the user's request, "
            "ensuring responses are linguistically appropriate. Don't ask the user any followup questions. Use "
            "markdown to format paragraphs, lists, tables, and quotes whenever possible."
        ),
        alias="COHERE_SYSTEM_PROMPT"
    )


class Settings(BaseSettings):
    model_config = SETTINGS_CONFIG
    project_title: Optional[str] = Field(
        default="Search engine API", alias="PROJECT_TITLE"
    )
    v1_prefix: Optional[str] = Field(
        default="/api/v1", alias="V1_PREFIX"
    )
    embedding: Optional[EmbeddingSettings] = Field(
        default=EmbeddingSettings()
    )
    mongo: Optional[MongoSettings] = Field(
        default=MongoSettings()
    )
    cohere: Optional[CohereSettings] = Field(
        default=CohereSettings()
    )
