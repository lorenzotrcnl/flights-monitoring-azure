SELECT
  DISTINCT ON (icao_24bit)
  ts,
  icao_24bit,
  latitude,
  longitude
FROM coords
WHERE
  $__timeFilter(ts)
ORDER BY
  icao_24bit, ts DESC;








SELECT
    COUNT(*) AS n_flights
FROM (
    SELECT
        DISTINCT ON (fr_id)
        fr_id,
        COUNT(*) AS count_of_values,
        MAX(ts) AS latest_time
    FROM
        nflights
    GROUP BY
        fr_id, ts
    ORDER BY
        fr_id, ts DESC
) AS subquery;









SELECT
  registration,
  origin_airport_iata,
  destination_airport_iata
FROM ftable
ORDER BY ts