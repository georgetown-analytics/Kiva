SELECT loan_id,To_timestamp(loans.posted_time,'YYYY-MM-DD HH24:MI:SS') 
       posted_time_actual,
		To_timestamp(loans.disburse_time,'YYYY-MM-DD HH24:MI:SS')
       disburse_time_actual,
		To_timestamp(loans.raised_time,'YYYY-MM-DD HH24:MI:SS')
       raised_time_actual
, DATE_PART('day',To_timestamp(loans.posted_time,'YYYY-MM-DD HH24:MI:SS')  - To_timestamp(loans.disburse_time,'YYYY-MM-DD HH24:MI:SS') )
disburse_to_posted_days
, DATE_PART('day',  To_timestamp(loans.raised_time,'YYYY-MM-DD HH24:MI:SS')   - To_timestamp(loans.posted_time,'YYYY-MM-DD HH24:MI:SS') )
posted_to_raised_days
, DATE_PART('day',  To_timestamp(loans.raised_time,'YYYY-MM-DD HH24:MI:SS')   - To_timestamp(loans.disburse_time,'YYYY-MM-DD HH24:MI:SS')  )
disbursed_to_raised_days
INTO loan_dates
FROM   loans
; 
