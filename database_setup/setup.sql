CREATE SCHEMA IF NOT EXISTS production;
CREATE TABLE production.trades (
    id INTEGER,
    ticker VARCHAR(5),
    price FLOAT,
    quantity INTEGER,
    status VARCHAR(15),
    source_file_name VARCHAR(256)

);

INSERT INTO production.trades (id, ticker, price, quantity, status, source_file_name)
VALUES 
    (1, 'TSLA', 100.00, 10, 'OPEN', '2023-06-23-trades-1'),
    (2, 'TSLA', 100.00, 10, 'OPEN', '2023-06-23-trades-2'),
    (1, 'TSLA', 100.00, 10, 'CLOSED', '2023-06-24-trades-1')
;