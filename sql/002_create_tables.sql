CREATE TABLE IF NOT EXISTS accidents (
            
            accident_id INT AUTO_INCREMENT PRIMARY KEY,

            accident_data DATE,

            location VARCHAR(100),

            weather VARCHAR (100),

            severity VARCHAR (100)

            );