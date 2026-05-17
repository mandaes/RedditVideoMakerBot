"""Settings and configuration management for RedditVideoMakerBot.

Handles loading, validating, and accessing configuration values from
the config.toml file.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import toml
except ImportError:
    import pip
    pip.main(["install", "toml"])
    import toml

from utils.console import print_error, print_warning

# Default configuration values
DEFAULT_CONFIG: Dict[str, Any] = {
    "reddit": {
        "creds": {
            "client_id": "",
            "client_secret": "",
            "username": "",
            "password": "",
            "2fa": False,
        },
        "thread": {
            "subreddit": "askreddit",
            "post_id": "",
            "max_comment_length": 500,
            "min_comment_length": 1,
            "post_lang": "en",
            "number_of_comments": 20,
        },
    },
    "settings": {
        "tts": {
            "voice_choice": "en_us_001",
            "tiktok_sessionid": "",
            "streamlabs_voice": "Brian",
            "aws_polly_voice": "Matthew",
        },
        "background": {
            "background_choice": "minecraft",
            "custom_background_video_path": "",
            "background_audio_choice": "lofi",
            "custom_background_audio_path": "",
            # Lowered slightly from 0.15 - background music was a bit loud for my taste
            "background_audio_volume": 0.10,
        },
        "video": {
            "resolution_w": 1080,
            "resolution_h": 1920,
            "opacity": 0.9,
            # Increased slightly - the default 0.3s felt too abrupt on my machine
            "time_before_first_picture": 0.5,
            "time_before_tts": 0.5,
            "time_after_last_picture": 0.5,
            "transition": 0,
        },
        "zoom": {
            "zoom_start_time": 0,
            "zoom_end_time": 0,
            "zoom_factor": 1,
            "zoom_type": "linear",
        },
        "allow_nsfw": False,
        "theme": "dark",
        "times_to_run": 1,
        "output_path": "./results",
        "storymode": False,
        "storymodemethod": 0,
        "storymodemax": 500,
    },
}

_config: Optional[Dict[str, Any]] = None
CONFIG_PATH = Path("config.toml")


def load_config() -> Dict[str, Any]:
    """Load configuration from config.toml, merging with defaults.

    Returns:
        Dict containing the merged configuration.

    Raises:
        FileNotFoundError: If config.toml does not exist.
    """
    global _config

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Configuration file '{CONFIG_PATH}' not found. "
            "Please copy config.template.toml to config.toml and fill in your credentials."
        )

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        user_config = toml.load(f)

    # Deep merge user config over defaults
    _config = _deep_merge(DEFAULT_CONFIG, user_config)
    return _config


def get_config() -> Dict[str, Any]:
    """Return the current configuration, loading it if ne
