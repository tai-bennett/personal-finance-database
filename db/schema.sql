PRAGMA foreign_keys = ON;

-- ======================================
-- raw ingestions
-- ======================================

CREATE TABLE IF NOT EXISTS raw_transations (
    raw_id TEXT PRIMARY KEY,
    source_bank TEXT NOT NULL,
    file_name TEXT NOT NULL,
    row_number INTEGER NOT NULL,
    ingestion_ts TEXT NOT NULL,
    file_has TEXT NOT NULL,
    raw_payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_raw_filehas
ON raw_transations (file_has);

-- ======================================
-- staging (normalized)
-- ======================================

CREATE TABLE IF NOT EXISTS staging_transactions (
    staging_id TEXT PRIMARY KEY,
    raw_id TEXT NOT NULL,
    source_bank TEXT NOT NULL,
    account_id TEXT,
    transaction_date TEXT NOT NULL,
    posted_date TEXT,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    ingestion_ts TEXT NOT NULL,
    FOREIGN KEY (raw_id) REFERENCES raw_transactions(raw_id)
);

-- ======================================
-- canoncial transactions
-- ======================================

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    fingerprint TEXT NOT NULL UNIQUE,
    account_id TEXT,
    transaction_date TEXT NOT NULL,
    posted_date TEXT,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL
);

-- ======================================
-- institutions and accounts
-- ======================================

CREATE TABLE IF NOT EXISTS institutions (
    institution_id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY,
    institution_id TEXT NOT NULL,
    account_type TEXT,
    masked_number TEXT,
    FOREIGN KEY (institution_id) REFERENCES institutions(institution_id)
);

