# Sector Canonicalization Mapping

To ensure deterministic scoring and consistent analysis across different data sources (NSE, screener.in, Groq), the following mappings must be used to normalize sector names.

## Mappings

| Original Sector Name | Canonical Name |
| :--- | :--- |
| BANK | BANKING |
| PRIVATE BANK | BANKING |
| PSU BANK | BANKING |
| IT SERVICES | IT |
| SOFTWARE | IT |
| TECHNOLOGY | IT |
| CONSUMER GOODS | FMCG |
| PACKAGED FOODS | FMCG |
| OIL & GAS | ENERGY |
| POWER | ENERGY |
| RENEWABLES | ENERGY |
| TELECOMMUNICATIONS | TELECOM |
| AUTOMOBILES | AUTO |
| AUTOMOTIVE | AUTO |
| CONSTRUCTION | INFRASTRUCTURE |
| CEMENT & AGGREGATES | CEMENT |
| FINANCIAL SERVICES | FINANCE |
| NBFC | FINANCE |
| PHARMACEUTICALS | PHARMA |
| HEALTHCARE | PHARMA |
| METALS & MINING | METALS |
| STELL | METALS |
| CONSUMER ELECTRONICS | CONSUMER DURABLES |

## Rules

1. All lookups must be case-insensitive.
2. If a sector is not in this mapping, it should default to its original name in UPPERCASE.
3. The scraping pipeline must apply this normalization before persisting to Supabase.
