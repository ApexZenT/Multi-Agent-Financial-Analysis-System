import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class PropertiesUtil:
    """Utility class for loading .properties-style configuration files."""

    PROPERTIES_DIR = Path(__file__).resolve().parent.parent
    _config = None

    def __init__(self, file_name: str) -> None:
        self.file_path = self.PROPERTIES_DIR / file_name
        self.properties = self._load_config()

    @classmethod
    def load_properties(cls):
        """Centralized configuration manager — loads global config once."""
        if cls._config is None:
            cls._config = PropertiesUtil(
                cls.PROPERTIES_DIR / "properties" / "global-settings.properties"
            )
            logger.info("Loaded global properties from %s", cls._config.file_path)
        return cls._config

    def _load_config(self) -> Dict[str, str]:
        """Load configuration from a file."""
        if not self.file_path.exists():
            logger.error("Config file not found: %s", self.file_path)
            raise FileNotFoundError(f"Config file not found: {self.file_path}")

        properties: Dict[str, str] = {}
        with self.file_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key_value = line.split("=", 1)
                    if len(key_value) == 2:
                        key, value = key_value
                        properties[key.strip()] = value.strip()
        logger.info("Loaded %d properties from %s", len(properties), self.file_path)
        return properties

    def get_property(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a property value by key."""
        if key not in self.properties and default is None:
            logger.warning("Property '%s' not found and no default provided.", key)
            raise KeyError(f"Property '{key}' not found and no default provided.")
        return self.properties.get(key, default)


# Example usage
if __name__ == "__main__":
    config_util = PropertiesUtil.load_properties()
    api_key = config_util.get_property("news_api_key", default="DEFAULT_KEY")
    logger.info("News API Key: %s", api_key)
