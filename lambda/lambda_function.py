import pg8000.native


def lambda_handler(event, context):
    con = pg8000.native.Connection("postgres", password="postgres")

    con.run(
        """
        INSERT INTO production.trades (id, ticker, price, quantity, status, source_file_name)
        VALUES 
            (1, 'AMZ', 100.00, 10, 'OPEN', '2023-06-23-trades-1'),
            (2, 'AMZ', 100.00, 10, 'OPEN', '2023-06-23-trades-2'),
            (1, 'AMZ', 100.00, 10, 'CLOSED', '2023-06-24-trades-1')
        ;"""
    )
