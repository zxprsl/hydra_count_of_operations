SELECT count(*) as 'Count', login
  FROM journal.query_journal j, conf.operator o
WHERE 1 = 1
      AND j.operator_id=o.id
      AND j.date > %(date1)s
      AND j.date < %(date2)s
 GROUP BY login