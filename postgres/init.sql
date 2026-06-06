CREATE TABLE market_data (
    id SERIAL PRIMARY KEY,
    trade_date DATE,
    company VARCHAR(100),
    rd_spending NUMERIC,
    revenue NUMERIC,
    revenue_growth NUMERIC,
    company_event VARCHAR(255),
    stock_impact NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);