"""Configuration schema definitions.

This module defines Pydantic models for validating and
parsing the application configuration, including Reddit
credentials, notification templates, and subreddit filters.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel
from pydantic_yaml import parse_yaml_raw_as


class SubredditConfig(BaseModel):
    """Configuration for filtering subreddit content.

    Attributes:
        title: List of strings to match against submission titles.
        not_title: List of strings that should not appear in titles.
        flair: List of strings to match against submission flairs.
        not_flair: List of strings that should not appear in flairs.
    """

    title: Optional[List[str]] = []
    not_title: Optional[List[str]] = []
    flair: Optional[List[str]] = []
    not_flair: Optional[List[str]] = []


class RedditConfig(BaseModel):
    """Reddit API and subreddit configuration.

    Attributes:
        client: Reddit API client ID.
        secret: Reddit API secret key.
        agent: User agent string for API requests.
        notification_title: Template for notification titles.
        notification_body: Template for notification bodies.
        subreddits: List of subreddit filter configurations.
    """

    client: str
    secret: str
    agent: str
    notification_title: Optional[str] = "{SUBREDDIT} - {TITLE}"
    notification_body: Optional[str] = "{URL}"
    subreddits: List[Dict[str, SubredditConfig]]


class Config(BaseModel):
    """Top-level application configuration.

    Attributes:
        apprise: List of Apprise notification endpoints.
        reddit: Reddit API and subreddit configuration.
    """

    apprise: List[str]
    reddit: RedditConfig

    @classmethod
    def from_yaml(cls, path: str) -> "Config":
        """Load configuration from a YAML file.

        Args:
            path: Path to the YAML configuration file.

        Returns:
            Config: Parsed configuration object.
        """
        with open(path, "r", encoding="utf-8") as f:
            return parse_yaml_raw_as(Config, f.read())
