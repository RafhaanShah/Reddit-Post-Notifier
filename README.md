# Reddit Post Notifier

Get notified for new Reddit posts that match your search criteria.

![](/assets/screenshot.jpg)

## Prerequisites
- A [Reddit](https://www.reddit.com/) account
- Reddit API `client_id` and `client_secret`, see [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) for more detailed instructions
- A notification service supported by [Apprise](https://github.com/caronc/apprise#popular-notification-services) and the required API keys or other configuration for your chosen services
- Have [Python](https://www.python.org/) 3.8+ or [Docker](https://www.docker.com/) installed

## Installation
This app can be used stand-alone and run with Python, or it is also available as a Docker image.
If using Python, install the requirements first:
`pip install -r requirements.txt`

## Configuration
The configuration is stored inside a yaml file, you can copy `config.yaml.example` into a new file `config.yaml` use that as a base, the following sections are all required:
1. Apprise configuration urls as a list, for your chosen providers
	```
	apprise:
	  - discord://webhook_id/webhook_token
	  - join://apikey/device
	  - slack://TokenA/TokenB/TokenC/
	```
2. Reddit configuration with your [app](https://www.reddit.com/prefs/apps) details, it is also [recommended](https://github.com/reddit-archive/reddit/wiki/API#rules) to put your username in the `agent` field but it can be anything you want
	```
	reddit:
	  client: xxxxxxxxxx
	  secret: xxxxxxxxxxxxxxxxxxxx_xxxxxxxxxx
	  agent: reddit-post-notifier (u/xxxxxx)
	```
3. Subreddit configuration with your desired search terms for each subreddit you want to monitor, the following example monitors r/GameDeals for any post that includes the words 'free' OR '100%' in the title (make sure this key appears under the `reddit` key, with [proper indentation](http://www.yamllint.com/), and using [single quotes](https://stackoverflow.com/questions/19109912/yaml-do-i-need-quotes-for-strings-in-yaml) if needed)
	```
	  subreddits:
	    gamedeals:
	      - 'free'
	      - '100%'
	```

### Optional
- `RPN_CONFIG` environment variable can be used to change the location of the config file, the default is `config.yaml` relative to where `app.py` is, `app/config.yaml` in the Docker image.
- `RPN_LOGGING` environment variable can be set to `TRUE` to enable logging each matched post to the console as well.
- [Docker-Compose](https://docs.docker.com/compose/) configuration:
```
version: "3.8"
services:
  reddit-post-notifier:
    container_name: reddit-post-notifier
    image: ghcr.io/rafhaanshah/reddit-post-notifier:latest
    restart: unless-stopped
    volumes:
        - ./config.yaml:/app/config.yaml	
```

## Usage
- Stand-alone:
	`python app.py`
- Docker:
	`docker run -v /path/to/your/config.yaml:/app/config.yaml ghcr.io/rafhaanshah/reddit-post-notifier:latest`

## Troubleshooting
- Check your `yaml` configuration is valid: http://www.yamllint.com
- Apprise does not log even if your configuration is invalid or not working, you can check if your urls work by installing the Apprise CLI: https://github.com/caronc/apprise/wiki/CLI_Usage
- Check the console logs for API errors, the app uses PRAW for accessing the Reddit API and you may find something in their docs: https://praw.readthedocs.io/en/latest/

## License
[MIT](https://choosealicense.com/licenses/mit/)
