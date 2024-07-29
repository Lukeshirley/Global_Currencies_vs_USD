-- join_data.sql
ATTACH DATABASE 'data/currency_performance.db' AS db;

CREATE TABLE IF NOT EXISTS combined_data AS
SELECT * FROM db.currency_data;
