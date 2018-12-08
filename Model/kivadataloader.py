class KivaDataLoader:

    def __init__(self):
        self.connected = False
        from sqlalchemy import create_engine
        from sqlalchemy import exc
        import dbconfig
        self.engine = create_engine(dbconfig.aws_connection_string)
        try:
            self.engine.connect()
            table_names = self.engine.table_names()
            print ('Connected to %s' % (dbconfig.aws_connection_string[dbconfig.aws_connection_string.index('@')+1:len(dbconfig.aws_connection_string)]))
            self.connected = True
        except exc.SQLAlchemyError:
            print("Connection Failed")

    def print_tables(self):
        table_names = self.engine.table_names()
        print(table_names)

    def get_clean_dataframe(self):
        import pandas as pd
        import numpy as np
        statement = """SELECT
        loans.loan_id
        ,loan_name
        ,CASE WHEN original_language = 'English'  THEN  1 ELSE 0 END AS language_english
        ,char_length(description) as description_length
        ,funded_amount
        ,loan_amount
        ,loans.status as status_loans
        ,CASE WHEN image_id IS NULL THEN  0 ELSE 1 END as loan_image_provided
        ,CASE WHEN video_id IS NULL THEN  0 ELSE 1 END  as loan_video_provided
        ,activity_name
        ,sector_name
        ,char_length(loan_use) loan_use_length
        ,country_code
        ,country_name
        ,currency_policy
        ,currency_exchange_coverage_rate
        ,currency
        ,CASE WHEN currency = 'USD' THEN 1 ELSE 0 END as currency_usd
        ,partner_id
        ,planned_expiration_time
        ,num_journal_entries
        ,num_bulk_entries
        ,CASE WHEN char_length(tags) > 0 THEN  1 ELSE 0 END tags_exist
        ,borrower_genders
        ,CASE WHEN borrower_pictured = 'FALSE' THEN 0 ELSE 1 END as atleast1_borrower_pictured
        ,repayment_interval
        ,distribution_model
        ,posted_time_actual
        ,disburse_to_posted_days
        ,posted_to_raised_days
        ,case when posted_to_raised_days < 8 then 0 when posted_to_raised_days < 15 then 1
        when posted_to_raised_days < 22 then 2 else 3 end as posted_to_raised_bins
        ,case when posted_to_raised_days < 8 then 1 else 0 end as raised_in_7_days_bit
        ,disbursed_to_raised_days
        ,partners.status as partner_status
        ,rating as partner_rating
        ,start_date as parner_start_date
        ,delinquency_rate as partner_delinquency_rate
        ,default_rate as partner_default_rate
        ,total_amount_raised as partner_total_amount_raised
        ,loans_posted as partner_loans_posted
        ,case when charges_fees_and_interest = 'TRUE' THEN 1 ELSE 0 END as partner_charges_fees_and_interest
        ,average_loan_size_percent_per_capita_income as partner_avg_loan_size_pct_per_capita_income
        ,loans_at_risk_rate as partner_loans_at_risk_rate
        ,currency_exchange_loss_rate as partner_loans_at_risk_rate
        ,CASE WHEN char_length(url) > 0 THEN  1 ELSE 0 END as partner_url_length
        ,portfolio_yield as partner_portfolio_yield
        ,profitability  as partner_profitability
         FROM loans
        inner join partners on partners.id = loans.partner_id
        inner join loan_dates on loans.loan_id = loan_dates.loan_id
        where loans.status = 'funded'
        and posted_to_raised_days >= 0 and posted_to_raised_days <= 30
        and borrower_genders <> 'None'
        """

        #print (statement)
        print ('The process takes about 5 minutes to run.')
        #and posted_time_actual >= make_date(2016, 6 ,1) and posted_time_actual <= make_date(2017, 5 ,31)

        try:
            cleanloans = pd.read_sql_query(statement, self.engine)
            cleanloans['num_borrowers_female'] = cleanloans['borrower_genders'].str.count('female')
            cleanloans['num_borrowers_male'] = cleanloans['borrower_genders'].str.count('^male') + cleanloans['borrower_genders'].str.count('\, male')
            cleanloans['num_borrowers'] = cleanloans['num_borrowers_female']+cleanloans['num_borrowers_male']
            cleanloans['num_borrowers_female_pct'] = (cleanloans['num_borrowers_female']*1.00)/cleanloans['num_borrowers']
            cleanloans = pd.concat([cleanloans,pd.get_dummies(cleanloans['sector_name'], prefix='sector_name')],axis=1)
            cleanloans.drop(['sector_name'],axis=1, inplace=True)

            cleanloans = pd.concat([cleanloans,pd.get_dummies(cleanloans['distribution_model'], prefix='distribution_model')],axis=1)
            cleanloans.drop(['distribution_model'],axis=1, inplace=True)

            cleanloans = pd.concat([cleanloans,pd.get_dummies(cleanloans['repayment_interval'], prefix='repayment_interval')],axis=1)
            cleanloans.drop(['repayment_interval'],axis=1, inplace=True)
        except:
            print ("***** statement for get_clean_dataframe failed *****")
            return

        #Add the borrowers code

        return cleanloans

    def create_or_rebuild_tbl_ddates(self,really):
        if really.upper() == 'Y' and self.connected == True:
            statement = """DROP TABLE if exists d_date;
            /*taken from https://medium.com/@duffn/creating-a-date-dimension-table-in-postgresql-af3f8e2941ac
            Nick Duffy
            */
            CREATE TABLE d_date
            (
              date_dim_id              INT NOT NULL,
              date_actual              DATE NOT NULL,
              epoch                    BIGINT NOT NULL,
              day_suffix               VARCHAR(4) NOT NULL,
              day_name                 VARCHAR(9) NOT NULL,
              day_of_week              INT NOT NULL,
              day_of_month             INT NOT NULL,
              day_of_quarter           INT NOT NULL,
              day_of_year              INT NOT NULL,
              week_of_month            INT NOT NULL,
              week_of_year             INT NOT NULL,
              week_of_year_iso         CHAR(10) NOT NULL,
              month_actual             INT NOT NULL,
              month_name               VARCHAR(9) NOT NULL,
              month_name_abbreviated   CHAR(3) NOT NULL,
              quarter_actual           INT NOT NULL,
              quarter_name             VARCHAR(9) NOT NULL,
              year_actual              INT NOT NULL,
              first_day_of_week        DATE NOT NULL,
              last_day_of_week         DATE NOT NULL,
              first_day_of_month       DATE NOT NULL,
              last_day_of_month        DATE NOT NULL,
              first_day_of_quarter     DATE NOT NULL,
              last_day_of_quarter      DATE NOT NULL,
              first_day_of_year        DATE NOT NULL,
              last_day_of_year         DATE NOT NULL,
              mmyyyy                   CHAR(6) NOT NULL,
              mmddyyyy                 CHAR(10) NOT NULL,
              weekend_indr             BOOLEAN NOT NULL
            );

            ALTER TABLE public.d_date ADD CONSTRAINT d_date_date_dim_id_pk PRIMARY KEY (date_dim_id);

            CREATE INDEX d_date_date_actual_idx
              ON d_date(date_actual);

            COMMIT;

            INSERT INTO d_date
            SELECT TO_CHAR(datum,'yyyymmdd')::INT AS date_dim_id,
                   datum AS date_actual,
                   EXTRACT(epoch FROM datum) AS epoch,
                   TO_CHAR(datum,'fmDDth') AS day_suffix,
                   TO_CHAR(datum,'Day') AS day_name,
                   EXTRACT(isodow FROM datum) AS day_of_week,
                   EXTRACT(DAY FROM datum) AS day_of_month,
                   datum - DATE_TRUNC('quarter',datum)::DATE +1 AS day_of_quarter,
                   EXTRACT(doy FROM datum) AS day_of_year,
                   TO_CHAR(datum,'W')::INT AS week_of_month,
                   EXTRACT(week FROM datum) AS week_of_year,
                   TO_CHAR(datum,'YYYY"-W"IW-') || EXTRACT(isodow FROM datum) AS week_of_year_iso,
                   EXTRACT(MONTH FROM datum) AS month_actual,
                   TO_CHAR(datum,'Month') AS month_name,
                   TO_CHAR(datum,'Mon') AS month_name_abbreviated,
                   EXTRACT(quarter FROM datum) AS quarter_actual,
                   CASE
                     WHEN EXTRACT(quarter FROM datum) = 1 THEN 'First'
                     WHEN EXTRACT(quarter FROM datum) = 2 THEN 'Second'
                     WHEN EXTRACT(quarter FROM datum) = 3 THEN 'Third'
                     WHEN EXTRACT(quarter FROM datum) = 4 THEN 'Fourth'
                   END AS quarter_name,
                   EXTRACT(isoyear FROM datum) AS year_actual,
                   datum +(1 -EXTRACT(isodow FROM datum))::INT AS first_day_of_week,
                   datum +(7 -EXTRACT(isodow FROM datum))::INT AS last_day_of_week,
                   datum +(1 -EXTRACT(DAY FROM datum))::INT AS first_day_of_month,
                   (DATE_TRUNC('MONTH',datum) +INTERVAL '1 MONTH - 1 day')::DATE AS last_day_of_month,
                   DATE_TRUNC('quarter',datum)::DATE AS first_day_of_quarter,
                   (DATE_TRUNC('quarter',datum) +INTERVAL '3 MONTH - 1 day')::DATE AS last_day_of_quarter,
                   TO_DATE(EXTRACT(isoyear FROM datum) || '-01-01','YYYY-MM-DD') AS first_day_of_year,
                   TO_DATE(EXTRACT(isoyear FROM datum) || '-12-31','YYYY-MM-DD') AS last_day_of_year,
                   TO_CHAR(datum,'mmyyyy') AS mmyyyy,
                   TO_CHAR(datum,'mmddyyyy') AS mmddyyyy,
                   CASE
                     WHEN EXTRACT(isodow FROM datum) IN (6,7) THEN TRUE
                     ELSE FALSE
                   END AS weekend_indr
            FROM (SELECT '1970-01-01'::DATE+ SEQUENCE.DAY AS datum
                  FROM GENERATE_SERIES (0,29219) AS SEQUENCE (DAY)
                  GROUP BY SEQUENCE.DAY) DQ
            ORDER BY 1;

            COMMIT;
                """

            print (statement)
                #and posted_time_actual >= make_date(2016, 6 ,1) and posted_time_actual <= make_date(2017, 5 ,31)
            try:
                self.engine.execute(statement)
            except:
                print ("statement for create_or_rebuild_tbl_ddates failed")

def create_or_rebuild_table_partners(self,really):
    if really.upper() == 'Y' and self.connected == True:
        statement = """DROP TABLE if exists partners;
        CREATE TABLE partners (
            id integer PRIMARY KEY,
            name character varying(98) NOT NULL,
            status character varying(8) NOT NULL,
            rating character varying(9) NOT NULL,
            start_date character varying(20) NOT NULL,
            delinquency_rate character varying(11) NOT NULL,
            default_rate character varying(11) NOT NULL,
            total_amount_raised integer NOT NULL,
            loans_posted integer NOT NULL,
            delinquency_rate_note character varying(614),
            default_rate_note character varying(630),
            portfolio_yield_note character varying(59),
            charges_fees_and_interest character varying(5),
            average_loan_size_percent_per_capita_income character varying(6) NOT NULL,
            loans_at_risk_rate numeric(12,9) NOT NULL,
            currency_exchange_loss_rate character varying(630) NOT NULL,
            url character varying(95),
            portfolio_yield numeric(4,1),
            profitability numeric(6,2)
        );
        COMMIT;
            """

        print (statement)
            #and posted_time_actual >= make_date(2016, 6 ,1) and posted_time_actual <= make_date(2017, 5 ,31)
        try:
            self.engine.execute(statement)
        except:
            print ("statement for create_or_rebuild_tbl_ddates failed")

        import requests
        import pandas as pd
        import json
        from pandas.io.json import json_normalize


        r = requests.get('https://api.kivaws.org/v1/partners.json&page=1')
        j = r.json()

        df = json_normalize(j['partners'])

        i = 2
        while i < 265:
            r = requests.get('https://api.kivaws.org/v1/partners.json&page=%d' % i)
            j = r.json()
            if len(j['partners']) == 0 :
                break
            df2 = json_normalize(j['partners'])
            frames = [df,df2]
            df = pd.concat(frames)
            i += 1

        partners = df
        partners.to_sql('partners', con=self.engine, if_exists='append')
