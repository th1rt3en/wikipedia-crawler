WITH
    url_0 AS (
        SELECT word, count
        FROM word_count
        WHERE url_index = 0
    ),

    url_1 AS (
        SELECT word, count
        FROM word_count
        WHERE url_index = 1
    ),

    total_freq AS (
        SELECT word, url_0.count + url_1.count AS count
        FROM url_0
        JOIN url_1
        USING (word)
    )

SELECT word, count
FROM total_freq
ORDER BY count DESC
LIMIT 1