PRAGMA foreign_keys = ON;

-- ======================================
-- raw ingestions
-- ======================================

CREATE TABLE IF NOT EXISTS raw_transactions (
    raw_id TEXT PRIMARY KEY,
    source_bank TEXT NOT NULL,
    file_name TEXT NOT NULL,
    row_number INTEGER NOT NULL,
    ingestion_ts TEXT NOT NULL,
    file_has TEXT NOT NULL,
    raw_payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_raw_file_has
ON raw_transactions (file_has);

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

-- ======================================
-- meta data: raw files
-- ======================================

CREATE TABLE IF NOT EXISTS raw_files (
    file_hash TEXT PRIMARY KEY,
    file_name TEXT,
    source_bank TEXT,
    file_size INTEGER,
    num_row INTEGER,
    ingestion_date TEXT
);

-- ======================================
-- categories & tags
-- ======================================

CREATE TABLE IF NOT EXISTS categories (
	category_id TEXT PRIMARY KEY,
	category_name TEXT NOT NULL
	);

CREATE TABLE IF NOT EXISTS category_rules (
	rule_id TEXT PRIMARY KEY,
	pattern_type TEXT NOT NULL,
	pattern TEXT NOT NULL,
	category_id NOT NULL,
	priority INTEGER DEFAULT 0,
	created_at TEXT NOT NULL,
	description TEXT,
	);

CREATE TABLE IF NOT EXISTS transaction_categories (
	categorization_id TEXT PRIMARY KEY,
	transaction_id TEXT NOT NULL,
	category_id TEXT NOT NULL,
	created_at TEXT NOT NULL
	);
