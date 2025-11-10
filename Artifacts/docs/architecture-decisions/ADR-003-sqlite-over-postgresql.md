# ADR-003: Use SQLite for Development, PostgreSQL-Ready for Production

## Status
Accepted

## Context
Database requirements:
- Local development simplicity
- Easy deployment for portfolio demonstration
- Production-ready architecture
- HIPAA-compliant data handling
- Support for complex queries (HEDIS temporal logic)

## Decision
Use SQLite for local development and portfolio demonstration, with PostgreSQL-ready architecture for production.

## Consequences

**Positive:**
- ✅ Zero setup for local development (SQLite is file-based)
- ✅ Easy deployment (no database server setup needed)
- ✅ PostgreSQL-compatible SQL (SQLAlchemy ORM abstracts differences)
- ✅ Fast for small-medium datasets (typical health plan portfolios)
- ✅ Production-ready architecture (can switch to PostgreSQL with config change)

**Negative:**
- ⚠️ Performance limits at scale (SQLite not ideal for 1M+ records with high concurrency)
- ⚠️ No concurrent write support (fine for portfolio demo, not for production)
- ⚠️ Limited advanced features (no full-text search, limited indexing options)

## Alternatives Considered

**PostgreSQL from Start:**
- ✅ Production-ready from day one
- ✅ Better performance at scale
- ✅ Advanced features (full-text search, JSON queries)
- ❌ Requires database server setup (Docker, local PostgreSQL, or cloud)
- ❌ More complex deployment for portfolio demo
- **Decision:** SQLite sufficient for portfolio demonstration, PostgreSQL-ready for production

**MySQL:**
- ✅ Common in production environments
- ❌ Less feature-rich than PostgreSQL
- ❌ Not as commonly used in healthcare analytics
- **Decision:** PostgreSQL is more feature-rich and better for analytics

## Implementation Notes
- Used SQLAlchemy ORM to abstract database differences
- Database connection string in config (`project/src/api/config.py`)
- Can switch to PostgreSQL by changing `DATABASE_URL` environment variable
- All queries use SQLAlchemy (no raw SQL), ensuring compatibility
- Database models in `project/src/database/models.py`

## Production Migration Path
To migrate to PostgreSQL:
1. Set `DATABASE_URL` to PostgreSQL connection string
2. Run migrations: `alembic upgrade head`
3. No code changes needed (SQLAlchemy handles differences)

