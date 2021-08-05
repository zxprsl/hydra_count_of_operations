WITH chg AS (
    -- Подписки
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM SI_SUBSCRIPTIONS
    UNION
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM HI_SUBSCRIPTIONS
    -- Оборудование
    UNION
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM SI_OBJECTS
    UNION
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM HI_OBJECTS
    -- Субъекты учета
    UNION
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM SI_SUBJECTS
    UNION
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM HI_COMPANIES
    UNION
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM HI_PERSONS
    UNION
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM HI_SUBJECTS
    -- Службы
    UNION
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM SI_SUBJ_SERVICES
    UNION
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM HI_SUBJ_SERVICES
    -- Документы
    UNION
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM SD_DOCUMENTS
    UNION
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM HD_DOCUMENTS
    UNION
    SELECT N_LOG_SESSION_ID, D_LOG_LAST_MOD
    FROM HD_INVOICES_T
)
SELECT COUNT(chg.N_LOG_SESSION_ID) "Кол-во", subj.VC_NAME "ФИО"
FROM chg,
     SS_SESSION_LOGS sess,
     SI_V_SUBJECTS subj
WHERE chg.N_LOG_SESSION_ID = sess.N_SESSION_ID
  AND sess.N_USER_ID = subj.N_SUBJECT_ID
  AND chg.D_LOG_LAST_MOD >= TO_DATE(:date1, 'YYYY-MM-DD')
  AND chg.D_LOG_LAST_MOD <= TO_DATE(:date2, 'YYYY-MM-DD')
GROUP BY subj.VC_NAME
ORDER BY 1 DESC
