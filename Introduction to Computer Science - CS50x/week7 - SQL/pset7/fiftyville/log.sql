-- Keep a log of any SQL queries you execute as you solve the mystery.
-- See the report of the crime
SELECT *
FROM crime_scene_reports
WHERE
    year = 2021
    AND month = 7
    AND day = 28
    AND street = 'Humphrey Street';

-- Interviews were made in the same day, lets see them.
SELECT *
FROM interviews
WHERE
    year = 2021
    AND month = 7
    AND day = 28;

-- witnesses are: Ruth, Eugene and Raymond
-- Ruth saw the thief leaving by car.
SELECT license_plate
    FROM bakery_security_logs
        WHERE
            year = 2021
            AND month = 7
            AND day = 28
            AND hour = 10
            AND activity = 'exit'
            AND minute < 26
            AND minute > 14;
-- | 5P2BI95       |
-- | 94KL13X       |
-- | 6P58WS2       |
-- | 4328GD8       |
-- | G412CB7       |
-- | L93JTIZ       |
-- | 322W7JE       |
-- | 0NTHK55       |
-- Eugene saw the thief withdrawing money before the crime.
SELECT name
    FROM people
        JOIN bank_accounts
            ON people.id = bank_accounts.person_id
            JOIN atm_transactions
                ON bank_accounts.account_number = atm_transactions.account_number
                WHERE
                    atm_transactions.year = 2021
                    AND atm_transactions.month = 7
                    AND atm_transactions.day = 28
                    AND atm_transactions.atm_location = 'Leggett Street'
                    AND atm_transactions.transaction_type = 'withdraw';
-- | Bruce   |
-- | Diana   |
-- | Brooke  |
-- | Kenny   |
-- | Iman    |
-- | Luca    |
-- | Taylor  |
-- | Benista |
-- Raymon saw the thief making a call under 1 minute, let's see who made a call and the name and license plate correspond to previous information.
SELECT name
    FROM phone_calls
        JOIN people
            ON phone_calls.caller = people.phone_number
            WHERE
                phone_calls.year = 2021
                AND phone_calls.month = 7
                AND phone_calls.day = 28
                AND phone_calls.duration < 60
                AND people.license_plate IN (
                    SELECT license_plate
                        FROM bakery_security_logs
                            WHERE
                                year = 2021
                                AND month = 7
                                AND day = 28
                                AND hour = 10
                                AND activity = 'exit'
                                AND minute < 26
                                AND minute > 14
                        )
                    AND people.name IN (
                        SELECT name
                               FROM people
                                JOIN bank_accounts
                                    ON people.id = bank_accounts.person_id
                                    JOIN atm_transactions
                                        ON bank_accounts.account_number = atm_transactions.account_number
                                        WHERE
                                            atm_transactions.year = 2021
                                            AND atm_transactions.month = 7
                                            AND atm_transactions.day = 28
                                            AND atm_transactions.atm_location = 'Leggett Street'
                                            AND atm_transactions.transaction_type = 'withdraw'
                         )
ORDER BY duration;
-- | Bruce |
-- | Diana |
-- Let's see who receivers were.
SELECT name
    FROM phone_calls
        JOIN people
            ON phone_calls.receiver = people.phone_number
            WHERE phone_calls.id IN (
                    SELECT phone_calls.id
                        FROM phone_calls
                            JOIN people
                                ON phone_calls.caller = people.phone_number
                                WHERE
                                    phone_calls.year = 2021
                                    AND phone_calls.month = 7
                                    AND phone_calls.day = 28
                                    AND phone_calls.duration < 60
                                    AND people.license_plate IN (
                                        SELECT license_plate
                                            FROM bakery_security_logs
                                                WHERE
                                                    year = 2021
                                                    AND month = 7
                                                    AND day = 28
                                                    AND hour = 10
                                                    AND activity = 'exit'
                                                    AND minute < 26
                                                    AND minute > 14
                                    )
                                        AND people.name IN (
                                            SELECT name
                                                FROM people
                                                    JOIN bank_accounts
                                                        ON people.id = bank_accounts.person_id
                                                        JOIN atm_transactions
                                                            ON bank_accounts.account_number = atm_transactions.account_number
                                                            WHERE
                                                                atm_transactions.year = 2021
                                                                AND atm_transactions.month = 7
                                                                AND atm_transactions.day = 28
                                                                AND atm_transactions.atm_location = 'Leggett Street'
                                                                AND atm_transactions.transaction_type = 'withdraw'
                                    )
            )
ORDER BY duration;
-- | Robin  |
-- | Philip |
-- Let's see who were on the flights after the robbery.
SELECT name, flight_id
    FROM people
    JOIN passengers
    ON people.passport_number = passengers.passport_number
    WHERE passengers.flight_id IN (
        SELECT flights.id
            FROM flights
            JOIN airports
                ON airports.id = flights.destination_airport_id
            WHERE flights.origin_airport_id =
                (SELECT id
                    FROM airports
                    WHERE city = 'Fiftyville')
            AND flights.year = 2021
            AND flights.month = 7
            AND 27 < flights.day < 30
    )
    AND people.name IN (
        SELECT name
    FROM phone_calls
        JOIN people
            ON phone_calls.caller = people.phone_number
            WHERE phone_calls.id IN (
                    SELECT phone_calls.id
                        FROM phone_calls
                            JOIN people
                                ON phone_calls.caller = people.phone_number
                                WHERE
                                    phone_calls.year = 2021
                                    AND phone_calls.month = 7
                                    AND phone_calls.day = 28
                                    AND phone_calls.duration < 60
                                    AND people.license_plate IN (
                                        SELECT license_plate
                                            FROM bakery_security_logs
                                                WHERE
                                                    year = 2021
                                                    AND month = 7
                                                    AND day = 28
                                                    AND hour = 10
                                                    AND activity = 'exit'
                                                    AND minute < 26
                                                    AND minute > 14
                                    )
                                        AND people.name IN (
                                            SELECT name
                                                FROM people
                                                    JOIN bank_accounts
                                                        ON people.id = bank_accounts.person_id
                                                        JOIN atm_transactions
                                                            ON bank_accounts.account_number = atm_transactions.account_number
                                                            WHERE
                                                                atm_transactions.year = 2021
                                                                AND atm_transactions.month = 7
                                                                AND atm_transactions.day = 28
                                                                AND atm_transactions.atm_location = 'Leggett Street'
                                                                AND atm_transactions.transaction_type = 'withdraw'
                                    )
            )
    );
-- | Diana | 18        |
-- | Diana | 54        |
-- | Bruce | 36        |
SELECT id, day, hour, minute FROM flights WHERE id = 18 OR id = 54 OR id = 36;
-- | 18 | 29  | 16   | 0      |
-- | 36 | 29  | 8    | 20     |
-- | 54 | 30  | 10   | 19     |
-- Bruce (in the flight with id = 36) went on the first plane, therefore I believe Bruce was the thief.
SELECT full_name, city
    FROM airports
    JOIN flights
    ON airports.id = flights.destination_airport_id
    WHERE flights.id = 36;
-- | LaGuardia Airport | New York City |