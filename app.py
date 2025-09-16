"""Stream new Reddit posts and notify for matching posts."""

import argparse
import datetime
import os
import re
import sys
import time

import apprise
import praw
import prawcore
from praw.exceptions import PRAWException
from prawcore.exceptions import PrawcoreException
from config_schema import Config


def main():
    """Run application."""
    parser = argparse.ArgumentParser(
        description="Stream new Reddit posts and notify for matching posts."
    )
    parser.add_argument(
        "--config",
        type=str,
        default=os.getenv("RPN_CONFIG", ""),
        help="Path to config file",
    )
    parser.add_argument(
        "--logging",
        type=str,
        default=os.getenv("RPN_LOGGING", ""),
        help="Enable logging (true/false)",
    )

    args = parser.parse_args()

    print("Starting Reddit Post Notifier")
    config = Config.from_yaml(args.config)
    apprise_client = get_apprise_client(config.apprise)
    reddit_client = get_reddit_client(
        config.reddit.client,
        config.reddit.secret,
        config.reddit.agent,
    )

    validate_subreddits(reddit_client, config.reddit.subreddits)
    stream_submissions(reddit_client, config.reddit, apprise_client, args.logging)


def stream_submissions(reddit, reddit_config, apprise_client, logging):
    """Monitor and process new Reddit submissions in given subreddits."""
    subreddits = reddit_config.subreddits
    subs = []
    for sub_dict in subreddits:
        for sub_name in sub_dict.keys():
            subs.append(sub_name)
            print(f"r/{sub_name}: {sub_dict[sub_name]}")
    subs_joined = "+".join(subs)
    subreddit = reddit.subreddit(subs_joined)

    while True:
        try:
            for submission in subreddit.stream.submissions(
                pause_after=None, skip_existing=True
            ):
                process_submission(submission, reddit_config, apprise_client, logging)

        except KeyboardInterrupt:
            sys.exit("\tStopping application, bye bye")

        except (
            PRAWException,
            PrawcoreException,
        ) as exception:
            print("Reddit API Error: ")
            print(exception)
            print("Pausing for 30 seconds...")
            time.sleep(30)


def process_submission(submission, reddit_config, apprise_client, logging):
    """Notify if given submission matches search."""
    title = submission.title
    flair = submission.link_flair_text
    sub = submission.subreddit.display_name
    processed = False

    for sub_dict in reddit_config.subreddits:
        for sub_name, config in sub_dict.items():
            if (
                sub.lower() == sub_name.lower()
                and not processed
                and matches(config, title, flair)
            ):
                processed = True
                notify(
                    apprise_client,
                    reddit_config,
                    submission,
                )
                if logging.lower() == "true":
                    print(
                        datetime.datetime.fromtimestamp(submission.created_utc),
                        " "
                        + "r/"
                        + sub
                        + ": "
                        + title
                        + ", "
                        + flair
                        + "\n"
                        + submission.permalink,
                    )


def matches(config, title, flair):
    """Return True if the item passes the include/exclude rules."""

    # include title → must match at least one
    if config.title:
        if not any(term.lower() in title.lower() for term in config.title):
            return False

    # exclude title → must NOT match any
    if config.not_title:
        if any(term.lower() in title.lower() for term in config.not_title):
            return False

    # include flair → must match at least one
    if config.flair and flair:
        if not any(term.lower() == flair.lower() for term in config.flair):
            return False

    # exclude flair → must NOT match any
    if config.not_flair and flair:
        if any(term.lower() == flair.lower() for term in config.not_flair):
            return False

    return True


def notify(apprise_client, reddit_config, submission):
    """Send apprise notification."""
    mapping = {
        "TITLE": submission.title,
        "SUBREDDIT": submission.subreddit.display_name,
        "URL": "https://www.reddit.com" + submission.permalink,
        "FLAIR": submission.link_flair_text or "",
    }
    title = render_template(reddit_config.notification_title, mapping)
    body = render_template(reddit_config.notification_body, mapping)
    apprise_client.notify(
        title=title,
        body=body,
    )


def get_reddit_client(cid, secret, agent):
    """Return PRAW Reddit instance."""
    return praw.Reddit(client_id=cid, client_secret=secret, user_agent=agent)


def get_apprise_client(config):
    """Return Apprise instance."""
    apprise_client = apprise.Apprise()
    for conf in config:
        apprise_client.add(conf)
    return apprise_client


def validate_subreddits(reddit, subreddits):
    """Validate subreddits."""
    for sub_dict in subreddits:
        for sub in sub_dict.keys():
            try:
                reddit.subreddit(sub).id
            except prawcore.exceptions.Redirect:
                sys.exit(f"Invalid Subreddit: {sub}")
            except (PRAWException, PrawcoreException) as exception:
                print("Reddit API Error: ")
                print(exception)


def render_template(template: str, mapping: dict) -> str:
    """
    Replace placeholders like {VAR} in the template string
    using the given mapping dict.
    - Keys in the mapping correspond to placeholders (case-sensitive).
    - Values can be constants or callables (lambdas/functions).
    - If a placeholder is not in the mapping, it is left unchanged.
    """

    def replacer(match):
        key = match.group(1)
        value = mapping.get(key)
        if callable(value):
            return str(value())
        if value is not None:
            return str(value)

        return f"{{{key}}}"  # leave unchanged if not found

    return re.sub(r"\{(\w+)\}", replacer, template)


if __name__ == "__main__":
    main()
