-- RTB Platform Database Schema

-- Campaigns table
CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    advertiser_id VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active', -- active, paused, completed
    budget_total DECIMAL(10,2) NOT NULL,
    budget_daily DECIMAL(10,2),
    budget_spent DECIMAL(10,2) DEFAULT 0,
    bid_price DECIMAL(6,4) NOT NULL, -- CPM bid price
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Campaign targeting rules
CREATE TABLE campaign_targeting (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    targeting_type VARCHAR(50) NOT NULL, -- geo, domain, language, device, etc.
    targeting_value TEXT NOT NULL, -- JSON array of values
    include_exclude VARCHAR(10) DEFAULT 'include' -- include or exclude
);

-- Creative banners
CREATE TABLE creatives (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    banner_url TEXT NOT NULL,
    click_url TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bid requests log
CREATE TABLE bid_requests (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(100) UNIQUE NOT NULL,
    imp_id VARCHAR(100) NOT NULL,
    auction_id VARCHAR(100),
    site_domain VARCHAR(255),
    site_page TEXT,
    user_country VARCHAR(10),
    user_language VARCHAR(10),
    device_type VARCHAR(20),
    banner_width INTEGER,
    banner_height INTEGER,
    floor_price DECIMAL(6,4),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT false
);

-- Bids placed
CREATE TABLE bids (
    id SERIAL PRIMARY KEY,
    bid_request_id INTEGER REFERENCES bid_requests(id),
    campaign_id INTEGER REFERENCES campaigns(id),
    creative_id INTEGER REFERENCES creatives(id),
    bid_price DECIMAL(6,4) NOT NULL,
    won BOOLEAN DEFAULT false,
    win_price DECIMAL(6,4),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Impressions served
CREATE TABLE impressions (
    id SERIAL PRIMARY KEY,
    bid_id INTEGER REFERENCES bids(id),
    campaign_id INTEGER REFERENCES campaigns(id),
    creative_id INTEGER REFERENCES creatives(id),
    cost DECIMAL(6,4),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clicks tracked
CREATE TABLE clicks (
    id SERIAL PRIMARY KEY,
    impression_id INTEGER REFERENCES impressions(id),
    campaign_id INTEGER REFERENCES campaigns(id),
    creative_id INTEGER REFERENCES creatives(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_dates ON campaigns(start_date, end_date);
CREATE INDEX idx_bid_requests_timestamp ON bid_requests(timestamp);
CREATE INDEX idx_bid_requests_domain ON bid_requests(site_domain);
CREATE INDEX idx_bids_campaign ON bids(campaign_id);
CREATE INDEX idx_impressions_campaign ON impressions(campaign_id);
CREATE INDEX idx_impressions_timestamp ON impressions(timestamp);
CREATE INDEX idx_clicks_campaign ON clicks(campaign_id);

-- Sample data
INSERT INTO campaigns (name, advertiser_id, budget_total, budget_daily, bid_price, start_date, end_date) VALUES
('Summer Sale Campaign', 'adv_001', 1000.00, 50.00, 2.5000, '2025-06-01', '2025-07-31'),
('Brand Awareness Q3', 'adv_002', 5000.00, 100.00, 1.8000, '2025-07-01', '2025-09-30');

INSERT INTO campaign_targeting (campaign_id, targeting_type, targeting_value) VALUES
(1, 'geo', '["US", "CA", "UK"]'),
(1, 'domain', '["news.com", "sports.com"]'),
(1, 'language', '["en"]'),
(2, 'geo', '["US"]'),
(2, 'device', '["mobile", "tablet"]');

INSERT INTO creatives (campaign_id, name, width, height, banner_url, click_url) VALUES
(1, 'Summer Banner 728x90', 728, 90, 'https://cdn.example.com/banners/summer_728x90.jpg', 'https://example.com/summer-sale'),
(1, 'Summer Banner 300x250', 300, 250, 'https://cdn.example.com/banners/summer_300x250.jpg', 'https://example.com/summer-sale'),
(2, 'Brand Banner Mobile', 320, 50, 'https://cdn.example.com/banners/brand_320x50.jpg', 'https://example.com/brand');