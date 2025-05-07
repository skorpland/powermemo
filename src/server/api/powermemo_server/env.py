"""
Initialize logger, encoder, and config.
"""

import os
import datetime
import json
from rich.logging import RichHandler
import yaml
import logging
import tiktoken
import dataclasses
from dataclasses import dataclass, field
from typing import Optional, Literal, Union
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from datetime import timezone
from typeguard import check_type
from .types import UserProfileTopic

load_dotenv()


class BillingStatus:
    free = "free"
    pro = "pro"
    usage_based = "usage_based"


BILLING_REFILL_AMOUNT_MAP = {
    BillingStatus.free: int(os.getenv("USAGE_TOKEN_LIMIT_ACTIVE", 0)) or None,
}


class ProjectStatus:
    ultra = "ultra"
    pro = "pro"
    active = "active"
    suspended = "suspended"


USAGE_TOKEN_LIMIT_MAP = {
    ProjectStatus.active: int(os.getenv("USAGE_TOKEN_LIMIT_ACTIVE", -1)),
    ProjectStatus.pro: int(os.getenv("USAGE_TOKEN_LIMIT_PRO", -1)),
    ProjectStatus.ultra: int(os.getenv("USAGE_TOKEN_LIMIT_ULTRA", -1)),
}


class ContanstTable:
    topic = "topic"
    sub_topic = "sub_topic"
    update_hits = "update_hits"


class TelemetryKeyName:
    insert_blob_request = "insert_blob_request"
    insert_blob_success_request = "insert_blob_success_request"
    llm_input_tokens = "llm_input_tokens"
    llm_output_tokens = "llm_output_tokens"
    has_request = "has_request"


@dataclass
class Config:
    # IMPORTANT!
    persistent_chat_blobs: bool = False
    use_timezone: Optional[
        Literal[
            "UTC", "America/New_York", "Europe/London", "Asia/Tokyo", "Asia/Shanghai"
        ]
    ] = None

    system_prompt: str = None
    buffer_flush_interval: int = 60 * 60  # 1 hour
    max_chat_blob_buffer_token_size: int = 1024
    max_profile_subtopics: int = 15
    max_pre_profile_token_size: int = 128
    llm_tab_separator: str = "::"
    cache_user_profiles_ttl: int = 60 * 20  # 20 minutes

    # LLM
    language: Literal["en", "zh"] = "en"
    llm_style: Literal["openai", "doubao_cache"] = "openai"
    llm_base_url: str = None
    llm_api_key: str = None
    llm_openai_default_query: dict[str, str] = None
    llm_openai_default_header: dict[str, str] = None
    best_llm_model: str = "gpt-4o-mini"
    summary_llm_model: str = None

    enable_event_embedding: bool = True
    embedding_provider: Literal["openai", "jina"] = "openai"
    embedding_api_key: str = None
    embedding_base_url: str = None
    embedding_dim: int = 1536
    embedding_model: str = "text-embedding-3-small"
    embedding_max_token_size: int = 8192

    additional_user_profiles: list[dict] = field(default_factory=list)
    overwrite_user_profiles: Optional[list[dict]] = None
    profile_strict_mode: bool = False
    profile_validate_mode: bool = True

    enable_event_summary: bool = True
    minimum_chats_token_size_for_event_summary: int = 256
    event_tags: list[dict] = field(default_factory=list)
    # Telemetry
    telemetry_deployment_environment: str = "local"

    @classmethod
    def _process_env_vars(cls, config_dict):
        """
        Process all environment variables for the config class.

        Args:
            cls: The config class
            config_dict: The current configuration dictionary

        Returns:
            Updated configuration dictionary with environment variables applied
        """
        # Ensure we have a dictionary to work with
        if not isinstance(config_dict, dict):
            config_dict = {}

        for field in dataclasses.fields(cls):
            field_name = field.name
            field_type = field.type
            env_var_name = f"POWERMEMO_{field_name.upper()}"
            if env_var_name in os.environ:
                env_value = os.environ[env_var_name]

                # Try to parse as JSON first
                try:
                    parsed_value = json.loads(env_value)
                    # Check if parsed value matches the type
                    try:
                        check_type(parsed_value, field_type)
                        config_dict[field_name] = parsed_value
                        continue
                    except TypeError:
                        # Parsed value doesn't match type, fall through to try raw string
                        pass
                except json.JSONDecodeError:
                    # Not valid JSON, fall through to try raw string
                    pass

                # Try the raw string
                try:
                    check_type(env_value, field_type)
                    config_dict[field_name] = env_value
                except TypeError as e:
                    LOG.warning(
                        f"Value for {env_var_name} is not compatible with field type {field_type}. Ignoring."
                    )

        return config_dict

    @classmethod
    def load_config(cls) -> "Config":
        if not os.path.exists("config.yaml"):
            overwrite_config = {}
        else:
            with open("config.yaml") as f:
                overwrite_config = yaml.safe_load(f)
                LOG.info(f"Load ./config.yaml")

        # Process environment variables
        overwrite_config = cls._process_env_vars(overwrite_config)

        # Filter out any keys from overwrite_config that aren't in the dataclass
        fields = {field.name for field in dataclasses.fields(cls)}
        filtered_config = {k: v for k, v in overwrite_config.items() if k in fields}
        overwrite_config = cls(**filtered_config)
        LOG.info(f"{overwrite_config}")
        return overwrite_config

    def __post_init__(self):
        assert self.llm_api_key is not None, "llm_api_key is required"
        if self.enable_event_embedding:
            if self.embedding_api_key is None and (
                self.llm_style == self.embedding_provider == "openai"
            ):
                # default to llm config if embedding_api_key is not set
                self.embedding_api_key = self.llm_api_key
                self.embedding_base_url = self.llm_base_url
            assert (
                self.embedding_api_key is not None
            ), "embedding_api_key is required for event embedding"

            if self.embedding_provider == "jina":
                self.embedding_base_url = (
                    self.embedding_base_url or "https://api.jina.ai/v1"
                )
                assert self.embedding_model in {
                    "jina-embeddings-v3",
                }, "embedding_model must be one of the following: jina-embeddings-v3"

        if self.additional_user_profiles:
            [UserProfileTopic(**up) for up in self.additional_user_profiles]
        if self.overwrite_user_profiles:
            [UserProfileTopic(**up) for up in self.overwrite_user_profiles]

    @property
    def timezone(self) -> timezone:
        if self.use_timezone is None:
            return datetime.datetime.now().astimezone().tzinfo

        # For named timezones, we need to use the datetime.timezone.ZoneInfo
        return ZoneInfo(self.use_timezone)


@dataclass
class ProfileConfig:
    language: Literal["en", "zh"] = None
    profile_strict_mode: bool | None = None
    profile_validate_mode: bool | None = None
    additional_user_profiles: list[dict] = field(default_factory=list)
    overwrite_user_profiles: Optional[list[dict]] = None

    enable_event_summary: bool = None
    event_tags: list[dict] = None

    def __post_init__(self):
        if self.language not in ["en", "zh"]:
            self.language = None
        if self.additional_user_profiles:
            [UserProfileTopic(**up) for up in self.additional_user_profiles]
        if self.overwrite_user_profiles:
            [UserProfileTopic(**up) for up in self.overwrite_user_profiles]

    @classmethod
    def load_config_string(cls, config_string: str) -> "Config":
        overwrite_config = yaml.safe_load(config_string)
        if overwrite_config is None:
            return cls()
        # Get all field names from the dataclass
        fields = {field.name for field in dataclasses.fields(cls)}
        # Filter out any keys from overwrite_config that aren't in the dataclass
        filtered_config = {k: v for k, v in overwrite_config.items() if k in fields}
        overwrite_config = cls(**filtered_config)
        return overwrite_config


# 1. Add logger
LOG = logging.getLogger("powermemo_server")
LOG.setLevel(logging.INFO)
console_handler = RichHandler()
LOG.addHandler(console_handler)

# 2. Add encoder for tokenize strings
ENCODER = tiktoken.encoding_for_model("gpt-4o")


# 3. Load config
CONFIG = Config.load_config()
