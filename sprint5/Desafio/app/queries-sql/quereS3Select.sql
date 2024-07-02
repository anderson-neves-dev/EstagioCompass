 SELECT
        COUNT(*),
        SUM(CAST(ilesos AS DECIMAL)),
        SUM(CAST(levemente_feridos AS DECIMAL)),
        SUM(CAST(moderadamente_feridos AS DECIMAL)),
        SUM(CAST(gravemente_feridos AS DECIMAL)),
        SUM(CAST(mortos AS DECIMAL)),
        SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL)),
        CASE WHEN 
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 100000 THEN UPPER('mais de 100 mil vítimas') 
         WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 50000 THEN UPPER('mais de 50 mil vitimas')
        WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 20000 THEN UPPER('mais de 20 mil vitimas')
        WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 10000 THEN UPPER('mais de 10 mil vitimas')
         WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 5000 THEN UPPER('mais de 5 mil vitimas')
         WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 1000 THEN UPPER('mais de mil vitimas')
         WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 100 THEN UPPER('mais de 100 vitimas')
         ELSE UPPER('MENOS DE 100 VITIMAS') END 

    FROM s3object s 
        where EXTRACT(YEAR FROM CAST(data AS TIMESTAMP)) = 2023 
        and 
        (UPPER(s.trecho) = UPPER('BR-116/SP') or UPPER(s.trecho) = UPPER('BR-116/RJ'))