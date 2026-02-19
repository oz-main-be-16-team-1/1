# -1-
django 프로젝트 1 팀입니다
 erDiagram
    users ||--o{ accounts : "has"
    accounts ||--o{ transactions : "records"

    users {
        INTEGRAL user_id PK
        VARCHAR(100) user_email
        VARCHAR(30) user_name
        VARCHAR(100) user_nickname
        VARCHAR(255) user_pw
        VARCHAR(15) user_phone
        DATETIME recent_login
        BOOLEAN setstaff
        BOOLEAN setadmin
        BOOLEAN setactive
        datetime create_at
    }

    accounts {
        INTEGRAL account_id PK
        VARCHAR(3) bank_code
        VARCHAR(30) account_number
        ENUM account_type "CHECKING, SAVINGS, FIXED, INSTALLMENT"
        DECIMAL(15_2) account_balance
        datetime created_at
        INTEGRAL user_id FK
    }

    transactions {
        INTEGRAL transaction_id PK
        DECIMAL(15_2) transaction_amount
        VARCHAR(255) transaction_history
        ENUM transaction_type "deposit, withdraw"
        ENUM transaction_method "CASH, BANK_TRANSFER, AUTO_TRANSFER, CARD"
        DECIMAL(15_2) balance_after
        DATETIME transaction_at
        datetime created_at
        INTEGRAL account_id FK
    }
