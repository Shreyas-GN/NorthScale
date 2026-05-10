import os
import csv
from typing import Dict, Optional
import sys

# Add backend to path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.supabase import get_supabase_client
from core.logging import logger

SECTOR_MAPPING = {
    "BANK": "BANKING",
    "PRIVATE BANK": "BANKING",
    "PSU BANK": "BANKING",
    "IT SERVICES": "IT",
    "SOFTWARE": "IT",
    "TECHNOLOGY": "IT",
    "CONSUMER GOODS": "FMCG",
    "PACKAGED FOODS": "FMCG",
    "OIL & GAS": "ENERGY",
    "POWER": "ENERGY",
    "RENEWABLES": "ENERGY",
    "TELECOMMUNICATIONS": "TELECOM",
    "AUTOMOBILES": "AUTO",
    "AUTOMOTIVE": "AUTO",
    "CONSTRUCTION": "INFRASTRUCTURE",
    "CEMENT & AGGREGATES": "CEMENT",
    "FINANCIAL SERVICES": "FINANCE",
    "NBFC": "FINANCE",
    "PHARMACEUTICALS": "PHARMA",
    "HEALTHCARE": "PHARMA",
    "METALS & MINING": "METALS",
    "STELL": "METALS",
    "CONSUMER ELECTRONICS": "CONSUMER DURABLES"
}

def canonicalize_sector(sector_name: str) -> str:
    """Apply deterministic canonicalization to sector names."""
    normalized = sector_name.strip().upper()
    return SECTOR_MAPPING.get(normalized, normalized)

def generate_slug(name: str) -> str:
    return name.lower().replace(" ", "-").replace("&", "and")

def seed_database():
    supabase = get_supabase_client()
    if not supabase:
        logger.error("Supabase client unavailable. Exiting.")
        return

    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs", "mvp_stock_universe.csv")
    
    if not os.path.exists(csv_path):
        logger.error(f"MVP Universe CSV not found at {csv_path}")
        return

    sectors = set()
    stocks = []

    # Parse CSV
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("ticker"):
                continue
            sector = canonicalize_sector(row["sector"])
            sectors.add(sector)
            stocks.append({
                "ticker": row["ticker"].upper(),
                "company_name": row["name"],
                "exchange": row["exchange"].upper(),
                "sector_name": sector
            })

    # 1. Seed Sectors
    logger.info(f"Seeding {len(sectors)} unique sectors...")
    sector_id_map: Dict[str, str] = {}
    for sector_name in sectors:
        slug = generate_slug(sector_name)
        # Check if exists
        res = supabase.table("sectors").select("id").eq("slug", slug).execute()
        if res.data:
            sector_id_map[sector_name] = res.data[0]["id"]
            logger.info(f"Sector {sector_name} already exists.")
        else:
            payload = {
                "name": sector_name,
                "slug": slug,
                "sector_type": "OTHER" # Defaults to OTHER, can be manually updated
            }
            # Attempt to map to standard enum
            if sector_name in ['BANKING', 'FMCG', 'PHARMA', 'IT', 'INFRA', 'AUTO', 'ENERGY', 'SAAS', 'TELECOM', 'REALESTATE']:
                payload["sector_type"] = sector_name
            elif sector_name == 'INFRASTRUCTURE':
                payload["sector_type"] = 'INFRA'
                
            ins_res = supabase.table("sectors").insert(payload).execute()
            if ins_res.data:
                sector_id_map[sector_name] = ins_res.data[0]["id"]
                logger.info(f"Inserted sector {sector_name}")

    # 2. Seed Stocks
    logger.info(f"Seeding {len(stocks)} stocks...")
    for s in stocks:
        res = supabase.table("stocks").select("id").eq("ticker", s["ticker"]).execute()
        if res.data:
            logger.info(f"Stock {s['ticker']} already exists.")
        else:
            payload = {
                "ticker": s["ticker"],
                "company_name": s["company_name"],
                "exchange": s["exchange"],
                "sector_id": sector_id_map.get(s["sector_name"])
            }
            ins_res = supabase.table("stocks").insert(payload).execute()
            if ins_res.data:
                logger.info(f"Inserted stock {s['ticker']}")

    logger.info("Database seeding complete.")

if __name__ == "__main__":
    seed_database()
