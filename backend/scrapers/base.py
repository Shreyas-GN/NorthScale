import abc
import requests
from typing import Dict, Any, Optional
from core.logging import logger

class BaseScraper(abc.ABC):
    """
    Abstract base class for all scrapers.
    Enforces the use of requests.Session and specific isolation strategies.
    """
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "application/json,text/plain,*/*"
        })
        self._is_bootstrapped = False

    @abc.abstractmethod
    def bootstrap_session(self) -> bool:
        """
        Initialize session cookies/tokens if required (e.g. visiting the homepage).
        Must be implemented by subclasses.
        """
        pass

    @abc.abstractmethod
    def fetch_data(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Fetch raw data for a given identifier (ticker, isin, etc).
        """
        pass

    def ensure_bootstrapped(self) -> bool:
        if not self._is_bootstrapped:
            logger.info(f"[{self.source_name}] Bootstrapping session...")
            self._is_bootstrapped = self.bootstrap_session()
            if not self._is_bootstrapped:
                logger.error(f"[{self.source_name}] Failed to bootstrap session.")
        return self._is_bootstrapped

    def get_json(self, url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        if not self.ensure_bootstrapped():
            return None
        
        try:
            response = self.session.get(url, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"[{self.source_name}] Request failed for URL {url}: {e}")
            return None
        except ValueError as e:
            logger.error(f"[{self.source_name}] Failed to parse JSON from {url}: {e}")
            return None
