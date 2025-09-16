from typing import List, Dict, Optional, Union
from pydantic import BaseModel
from pydantic_yaml import parse_yaml_raw_as

class SubredditConfig(BaseModel):
    title: Optional[List[str]] = []
    not_title: Optional[List[str]] = []
    flair: Optional[List[str]] = []
    not_flair: Optional[List[str]] = []


class RedditConfig(BaseModel):
    client: str
    secret: str
    agent: str
    notification_title: Optional[str] = "{SUBREDDIT} - {TITLE}"
    notification_body: Optional[str] = "{URL}"
    subreddits: List[Dict[str, SubredditConfig]]


class Config(BaseModel):
    apprise: List[str]
    reddit: RedditConfig

    @classmethod
    def from_yaml(cls, path: str) -> "Config":
        with open(path, "r", encoding="utf-8") as f:
            return parse_yaml_raw_as(Config, f.read())
