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
            "background_audio_volume": 0.15,
        },
        "video": {
            "resolution_w": 1080,
            "resolution_h": 1920,
            "opacity": 0.9,
            "time_before_first_picture": 0.3,
            "time_before_tts": 0.5,
            "time_after_last_picture": 0.3,
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
    """Return the current configuration, loading it if necessary."""
    global _config
    if _config is None:
        _config = load_config()
    return _config


def get(key_path: str, default: Any = None) -> Any:
    """Get a configuration value using dot-notation key path.

    Args:
        key_path: Dot-separated path to the config value (e.g. 'reddit.creds.client_id').
        default: Value to return if the key is not found.

    Returns:
        The configuration value, or default if not found.
    """
    config = get_config()
    keys = key_path.split(".")
    value = config
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    return value


def _deep_merge(base: Dict, override: Dict) -> Dict:
    """Recursively merge override dict into base dict.

    Args:
        base: The base dictionary with default values.
        override: The dictionary with overriding values.

    Returns:
        Merged dictionary.
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result
