from typing import Dict, Any, Optional
from scrapers.base import BaseScraper
from core.logging import logger

class NSEScraper(BaseScraper):
    """
    NSE India source scraper.
    Uses a requests session bootstrapped via the NSE homepage.
    """
    def __init__(self):
        super().__init__("NSE")
        self.base_url = "https://www.nseindia.com"
        self.session.headers.update({
            "Referer": "https://www.nseindia.com/"
        })

    def bootstrap_session(self) -> bool:
        """
        Visits the NSE homepage to obtain Akamai cookies.
        """
        try:
            res = self.session.get(self.base_url, timeout=15)
            res.raise_for_status()
            logger.info("[NSE] Session bootstrapped successfully.")
            return True
        except Exception as e:
            logger.error(f"[NSE] Failed to bootstrap session: {e}")
            return False

    def fetch_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Fetches equity quote data from the NSE API.
        """
        url = f"{self.base_url}/api/quote-equity"
        params = {"symbol": ticker}
        return self.get_json(url, params=params)

    def fetch_corporate_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Fetches corporate info (e.g., shareholding pattern overview) if needed.
        """
        url = f"{self.base_url}/api/corp-info"
        params = {"symbol": ticker}
        return self.get_json(url, params=params)
