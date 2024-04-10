# Sync Liked Tweets to Notion

## Overview

`favorite-tweets` is a Python-based project that automates the process of fetching your latest favorite tweets from
Twitter and adding them to a Notion table. This is ideal for keeping a record of tweets you find interesting or want to
save for future reference.

## Prerequisites

- A Twitter Developer account with an app to get your API keys.
- Access to the Notion API with an integration.
- Python 3.6+ installed on your computer.
- Pipenv for handling project dependencies and virtual environments.

## Installation & Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ichironagata/favorite-tweets.git
    cd favorite-tweets
    ```

2. **Install dependencies:**
   Use Pipenv to create a virtual environment and install the necessary packages.
    ```bash
    pipenv install
    ```

3. **Set up environment variables:**
   Rename `.env.example` to `.env` and fill in your Twitter and Notion API keys.

## Usage

1. **Run the script:**
   Activate the Pipenv shell and execute the main script:
    ```bash
    pipenv shell
    python sync_tweets_to_notion.py
    ```

2. **Exit the virtual environment:**
   After you're done, you can exit the virtual environment by running:
    ```bash
    exit
    ```

## Running Tests

This project uses `unittest`, a built-in Python testing framework, for running unit tests.

To run the tests, navigate to the project directory and run the following command:

```bash
python -m unittest test_sync_liked_tweets_to_notion.py
```
