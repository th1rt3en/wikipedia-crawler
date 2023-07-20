SELECT word, AVG(count) AS avg_count
FROM word_count
GROUP BY word ORDER BY avg_count DESC