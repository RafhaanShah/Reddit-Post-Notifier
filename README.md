# Reddit Post Notifier

Get notified for new Reddit posts that match your search criteria.

![screenshot](/assets/screenshot.jpg)

## Prerequisites

- A [Reddit](https://www.reddit.com/) account
- Reddit API `client_id` and `client_secret`, see [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) for more detailed instructions
- A notification service supported by [Apprise](https://github.com/caronc/apprise#popular-notification-services) and the required API keys or other configuration for your chosen services

## Building

Install Requirements:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Upgrade Dependencies:

```shell
pip install pipreqs
pip install --upgrade -r requirements.txt
pipreqs --force --ignore .venv
```

## Installation

- If you have Python installed, you can clone the repository and directly run the Python file
- You can download the latest release artifact from [GitHub Releases](https://github.com/RafhaanShah/Reddit-Post-Notifier/releases)
- If you have Docker installed, you can run the Docker image

## Configuration

- The configuration is stored inside a yaml file, you can copy `config.yaml.example` into a new file `config.yaml` use that as a base, the following sections are all required:

1. Apprise configuration urls as a list, for your chosen providers

   ```yaml
   apprise:
     - discord://webhook_id/webhook_token
     - join://apikey/device
     - slack://TokenA/TokenB/TokenC/
   ```

1. Reddit configuration with your [app](https://www.reddit.com/prefs/apps) details, it is also [recommended](https://github.com/reddit-archive/reddit/wiki/API#rules) to put your username in the `agent` field but it can be anything you want. You can also configure the `notification_title` and `notification_body` with placeholders for details of the post. Available placeholders for notifications are: - `{TITLE}` - `{SUBREDDIT}` - `{URL}` - `{FLAIR}`

   ```yaml
   reddit:
     client: xxxxxxxxxx
     secret: xxxxxxxxxxxxxxxxxxxx_xxxxxxxxxx
     agent: reddit-post-notifier (u/xxxxxx)
     notification_title: "{SUBREDDIT} - {TITLE}"
     notification_body: "{URL}"
   ```

1. Subreddit configuration with your desired filters for each subreddit you want to monitor, make sure this key appears under the `reddit` key, with [proper indentation](http://www.yamllint.com/), and using [single quotes](https://stackoverflow.com/questions/19109912/yaml-do-i-need-quotes-for-strings-in-yaml) if needed. All filters are optional. Filters are additive so if you include 3 filters they ALL must all match for the post to pass. The following options are supported:
   - `title`: filters posts to those that DO include ANY of the listed terms in the title (case insensitive)

     ```yaml
     subreddits:
       - gamedeals:
         title:
           - "free"
           - "100%"
     ```

   - `not_title`: filters posts to those that DO NOT include ANY of the listed terms in the title (case insensitive)

     ```yaml
     subreddits:
       - hmm:
         not_title:
           - "hmm"
           - "mmh"
     ```

   - `flair`: filters posts to those that DO include ANY of the listed terms in the flair (case insensitive)

     ```yaml
     subreddits:
       - Catswhoyell:
         flair:
           - "Scream Team"
           - "Human Conversationalist"
     ```

   - `not_flair`: filters posts to those that DO NOT include ANY of the listed terms in the flair (case insensitive)

     ```yaml
     subreddits:
       - ATBGE:
         not_flair:
           - "Fashion"
           - "Decor"
     ```

   - The following example will match posts in `r/NotARealSub` where all of the following are true:
     1. The title includes any of: `Hello`, `Hi`
     2. The title does not include any of `Bye`, `Ciao`
     3. The flair is any of `Cool Post`,`Good Post`
     4. The flair is not any of `Boring Post`, `Bad Post`

     ```yaml
     subreddits:
       - NotARealSub:
         title:
           - "Hello"
           - "Hi"
         not_title:
           - "Bye"
           - "Ciao"
         flair:
           - "Cool Post"
           - "Good Post"
         not_flair:
           - "Boring Post"
           - "Bad Post"
     ```

### Optional

- `RPN_CONFIG` environment variable or `--config` argument can be used to change the location of the config file, the default is `config.yaml` relative to where `app.py` is, `app/config.yaml` in the Docker image.
- `RPN_LOGGING` environment variable or `--logging` argument can be set to `TRUE` to enable logging each matched post to the console as well.

## Usage

- Python: `python app.py`
- Executable: `./rpn`
- Docker:
  `docker run -v /path/to/your/config.yaml:/app/config.yaml ghcr.io/rafhaanshah/reddit-post-notifier:latest`
- Docker-Compose:

```yaml
services:
  reddit-post-notifier:
    container_name: reddit-post-notifier
    image: ghcr.io/rafhaanshah/reddit-post-notifier:latest
    restart: unless-stopped
    volumes:
      - ./config.yaml:/app/config.yaml
```

## Troubleshooting

- Check your `yaml` configuration is valid: http://www.yamllint.com
- Apprise does not log even if your configuration is invalid or not working, you can check if your urls work by installing the Apprise CLI: https://github.com/caronc/apprise/wiki/CLI_Usage
- Check the console logs for API errors, the app uses PRAW for accessing the Reddit API and you may find something in their docs: https://praw.readthedocs.io/en/latest/

## License

[MIT](https://choosealicense.com/licenses/mit/)
