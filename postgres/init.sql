CREATE TABLE raw_market_data (
    id SERIAL PRIMARY KEY,
    trade_date DATE,
    company VARCHAR(100),
    rd_spending FLOAT,
    revenue FLOAT,
    revenue_growth FLOAT,
    company_event TEXT,
    stock_impact FLOAT
);

CREATE TABLE clean_market_data (
    id SERIAL PRIMARY KEY,
    trade_date DATE,
    company VARCHAR(100),
    rd_spending FLOAT,
    revenue FLOAT,
    revenue_growth FLOAT,
    company_event TEXT,
    stock_impact FLOAT
);

DROP TABLE IF EXISTS anomaly_results;
CREATE TABLE anomaly_results (
    id SERIAL PRIMARY KEY,
    trade_date DATE,
    company VARCHAR(100),
    stock_impact FLOAT,
    z_score FLOAT,
    anomaly_flag BOOLEAN,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(trade_date, company)
);
