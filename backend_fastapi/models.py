"""
emailもしくは会社idと従業員idで一意に識別できるようにする
パスワードはハッシュ化して保存する
"""

import datetime
import os
import random
import string
import time

import dotenv
import psycopg2


class Models():
    def __init__(self):
        # postgresqlに接続する
        dotenv_path = os.path.join(os.path.dirname(__file__), 'db.env')
        dotenv.load_dotenv()
        dotenv.load_dotenv(dotenv_path)
        MODE = os.getenv("MODE")
        print(f"============================MODE: {MODE}============================")
        if MODE == "dev":
            self.host = os.getenv("LOCAL_DB_HOST")
            self.port = os.getenv("LOCAL_DB_PORT")
            self.password = os.getenv("LOCAL_DB_PASSWORD")
            self.user = os.getenv("LOCAL_DB_USER")
            self.database = os.getenv("LOCAL_DB_DATABASE")
        elif MODE == "prod":
            self.host = os.getenv("POSTGRES_HOST")
            self.port = os.getenv("POSTGRES_PORT")
            self.password = os.getenv("POSTGRES_PASSWORD")
            self.user = os.getenv("POSTGRES_USER")
            self.database = os.getenv("POSTGRES_DB")
        # TODO: 接続できるまで繰り返す
        print(f"=============={self.host}:{self.port}に接続します。==============")
        print(f"==============ユーザー名: {self.user}==============")
        print(f"==============データベース名: {self.database}==============")
        try:
            with self.get_connection():
                print("postgresqlに接続しました。")
                pass
        except psycopg2.OperationalError:
            # 数秒待って再接続
            sleep_time = 5
            print(f"postgresqlに接続できませんでした。{sleep_time}秒後に再接続します。")
            time.sleep(sleep_time)
            with self.get_connection():
                pass
        self.create_companies_tables()

    def get_connection(self):
        # データベースに接続する
        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            password=self.password,
            user=self.user,
            database=self.database
        )
        return conn

    def execute_query(self, sql, params=None):
        """
        SQL文を実行する関数

        Parameters
        ----------
        sql : str
            SQL文
        params : tuple
            SQL文に埋め込むパラメータ

        Returns
        -------
        None
        """
        data = []
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    # もしSELECT文だったら、結果を返す
                    if sql.startswith("SELECT"):
                        data = cursor.fetchall()
                conn.commit()
        except psycopg2.Error as e:
            print(f"クエリの実行に失敗しました: {e}")
        return data

    def create_companies_tables(self):
        # テーブルを作成する
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # 会社テーブルを作成
                sql = """
                    CREATE TABLE IF NOT EXISTS companies (
                        company_id SERIAL PRIMARY KEY,
                        company_name VARCHAR(30),
                        company_email VARCHAR(30) UNIQUE,
                        company_login_password VARCHAR(30),
                        UNIQUE (company_id, company_email)
                    )
                """
                cursor.execute(sql)
            conn.commit()

    def create_other_tables(self):
        # テーブルを作成する
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # WORK_TYPEのenumが存在するか確認
                sql = """
                    SELECT EXISTS (
                        SELECT 1
                        FROM pg_type
                        WHERE typname = 'WORK_TYPE'
                    )
                """
                type_exists = cursor.execute(sql)
                cursor.execute(sql)
            conn.commit()
            if not type_exists:
                with conn.cursor() as cursor:
                    # WORK_TYPEのenumを作成
                    sql = """
                        CREATE TYPE WORK_TYPE AS ENUM (
                            'DAY_OFF', 'WORKDAY', 'HOLIDAY', 'ALL_DAY_LEAVE', 'MORNING_LEAVE', 'AFTERNOON_LEAVE'
                        )
                    """
                    cursor.execute(sql)
                conn.commit()
            with conn.cursor() as cursor:
                # workpalceのenumが存在するか確認
                sql = """
                    SELECT EXISTS (
                        SELECT 1
                        FROM pg_type
                        WHERE typname = 'WORKPLACE'
                    )
                """
                type_exists = cursor.execute(sql)
                cursor.execute(sql)
            conn.commit()
            if not type_exists:
                with conn.cursor() as cursor:
                    # workpalceのenumを作成
                    sql = """
                        CREATE TYPE WORKPLACE AS ENUM (
                            'OFFICE', 'HOME', 'OTHER'
                        )
                    """
                    cursor.execute(sql)
                conn.commit()
            with conn.cursor() as cursor:
                # statusのenumが存在するか確認
                sql = """
                    SELECT EXISTS (
                        SELECT 1
                        FROM pg_type
                        WHERE typname = 'STATUS'
                    )
                """
                type_exists = cursor.execute(sql)
                cursor.execute(sql)
            conn.commit()
            if not type_exists:
                with conn.cursor() as cursor:
                    # statusのenumを作成
                    sql = """
                        CREATE TYPE STATUS AS ENUM (
                            'REQUESTED', 'APPROVED', 'REJECTED'
                        )
                    """
                    cursor.execute(sql)
                conn.commit()
            with conn.cursor() as cursor:
                # authorityのenumが存在するか確認
                sql = """
                    SELECT EXISTS (
                        SELECT 1
                        FROM pg_type
                        WHERE typname = 'AUTHORITY'
                    )
                """
                type_exists = cursor.execute(sql)
                cursor.execute(sql)
            conn.commit()
            if not type_exists:
                with conn.cursor() as cursor:
                    # authorityのenumを作成
                    sql = """
                        CREATE TYPE AUTHORITY AS ENUM (
                            'ADMIN', 'USER'
                        )
                    """
                    cursor.execute(sql)
                conn.commit()

            with conn.cursor() as cursor:
                # カレンダーテーブルを作成
                sql = """
                    CREATE TABLE IF NOT EXISTS calendar (
                        date DATE,
                        dow int,
                        work_type WORK_TYPE,
                        PRIMARY KEY (date)
                    )
                """
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 従業員テーブルを作成
                sql = """
                    CREATE TABLE IF NOT EXISTS employees (
                        company_id INTEGER,
                        employee_id SERIAL,
                        employee_name VARCHAR(30),
                        employee_email VARCHAR(30),
                        employee_login_password VARCHAR(30),
                        authority AUTHORITY,
                        commuting_expenses INTEGER,
                        UNIQUE (company_id, employee_id),
                        UNIQUE (company_id, employee_email),
                        FOREIGN KEY (company_id) REFERENCES companies(company_id)
                    )
                """
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 勤怠記録テーブルを作成
                # delete: work_record_idはいらないかも
                sql = """
                    CREATE TABLE IF NOT EXISTS work_records (
                        work_record_id SERIAL PRIMARY KEY,
                        company_id INTEGER,
                        employee_id INTEGER,
                        work_date DATE,
                        start_work_at TIME,
                        finish_work_at TIME,
                        start_break_at TIME,
                        finish_break_at TIME,
                        start_overwork_at TIME,
                        finish_overwork_at TIME,
                        workplace WORKPLACE,
                        work_contents VARCHAR(50),
                        UNIQUE (company_id, employee_id, work_date),
                        FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id)
                    )
                """
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 勤怠修正記録テーブルを作成
                sql = """
                    CREATE TABLE IF NOT EXISTS correction_records (
                        correction_record_id SERIAL PRIMARY KEY,
                        company_id INTEGER,
                        employee_id INTEGER,
                        work_date TIMESTAMP,
                        start_work_at TIME,
                        finish_work_at TIME,
                        start_break_at TIME,
                        finish_break_at TIME,
                        start_overwork_at TIME,
                        finish_overwork_at TIME,
                        workplace WORKPLACE,
                        work_contents VARCHAR(50),
                        status STATUS,
                        confirmed_at TIMESTAMP,
                        reject_reason VARCHAR(50),
                        UNIQUE (company_id, correction_record_id),
                        FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id)
                    )
                """
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 有休カレンダーテーブルを作成
                sql = """
                    CREATE TABLE IF NOT EXISTS paid_leaves (
                        company_id INTEGER,
                        employee_id INTEGER,
                        date DATE,
                        work_type WORK_TYPE,
                        UNIQUE (company_id, employee_id, date),
                        FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id)
                    )
                """
            conn.commit()
            with conn.cursor() as cursor:
                # 有休申請記録テーブルを作成
                sql = """
                    CREATE TABLE IF NOT EXISTS paid_leaves_records (
                        paid_leave_record_id SERIAL PRIMARY KEY,
                        company_id INTEGER,
                        employee_id INTEGER,
                        paid_leave_date DATE,
                        work_type WORK_TYPE,
                        paid_leave_reason VARCHAR(50),
                        requested_at TIMESTAMP,
                        status STATUS,
                        confirmed_at TIMESTAMP,
                        reject_reason VARCHAR(50),
                        UNIQUE (company_id, paid_leave_record_id),
                        FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id)
                    )
                """
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 有休日数テーブルを作成
                sql = """
                    CREATE TABLE IF NOT EXISTS paid_leaves_days (
                        company_id INTEGER,
                        employee_id INTEGER,
                        year INTEGER,
                        max_paid_leave_days FLOAT,
                        used_paid_leave_days FLOAT,
                        UNIQUE (company_id, employee_id, year),
                        FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id)
                    )
                """
                cursor.execute(sql)
            conn.commit()

    ######################################################################################
    # 管理者だけができる操作
    ######################################################################################
    def add_company(self, company_name, company_email, company_login_password):
        # 会社を追加する
        # add: ハッシュ化したパスワードをデータベースに保存する
        # add: sessionにcompany_idを保存する
        # add: company_login_passwordを隠して通信する
        sql = "INSERT INTO companies (company_name, company_email, company_login_password) VALUES (%s, %s, %s)"
        self.execute_query(sql, (company_name, company_email, company_login_password))

        # 会社IDを取得する
        sql = "SELECT company_id, company_name, company_email, company_login_password\
            FROM companies\
            WHERE company_name = %s AND company_email = %s"
        data = self.execute_query(sql, (company_name, company_email))[0]
        # company_login_passwordの文字数を取得して、*をかける
        company_login_password_length = len(data[3])
        hidden_company_login_password = "*" * company_login_password_length

        self.create_other_tables()

        # add: calendarに日付と曜日を追加する
        sql = """
            INSERT INTO calendar (date, dow, work_type)
            SELECT
                calendar_date,
                EXTRACT(ISODOW FROM calendar_date),
                CASE
                    WHEN EXTRACT(ISODOW FROM calendar_date) = 6 THEN 'DAY_OFF'::WORK_TYPE
                    WHEN EXTRACT(ISODOW FROM calendar_date) = 7 THEN 'DAY_OFF'::WORK_TYPE
                    ELSE 'WORKDAY'::WORK_TYPE
                END
            FROM
                generate_series(current_date::DATE, current_date::DATE + '1 year'::INTERVAL, '1 day') AS calendar_date
            ;
        """
        self.execute_query(sql)

        return {
            "company_id": data[0],
            "company_name": data[1],
            "company_email": data[2],
            "company_login_password": hidden_company_login_password,
        }

    def get_company(self, company_id):
        # 会社情報を取得する
        sql = "SELECT company_id, company_name, company_email FROM companies WHERE company_id = %s"
        data = self.execute_query(sql, (company_id,))[0]
        return {
            "company_id": data[0],
            "company_name": data[1],
            "company_email": data[2],
        }

    def update_company(self, company_id, company_name: str = "", company_email: str = "", old_company_login_password: str = "", new_company_login_password: str = ""):
        # 会社情報を更新する
        # add: ハッシュ化したパスワードをデータベースに保存する
        sql = "SELECT company_login_password FROM companies WHERE company_id = %s"
        company_login_password = self.execute_query(sql, (company_id,))[0][0]
        if company_login_password != old_company_login_password:
            return {
                "error": "パスワードが間違っています",
            }
        # 空じゃないものだけ更新する
        if company_name != "":
            sql = "UPDATE companies SET company_name = %s WHERE company_id = %s"
            self.execute_query(sql, (company_name, company_id))
        if company_email != "":
            sql = "UPDATE companies SET company_email = %s WHERE company_id = %s"
            self.execute_query(sql, (company_email, company_id))
        if new_company_login_password != "":
            sql = "UPDATE companies SET company_login_password = %s WHERE company_id = %s"
            self.execute_query(sql, (new_company_login_password, company_id))
        # 会社情報を取得する
        sql = "SELECT company_id, company_name, company_email FROM companies WHERE company_id = %s"
        data = self.execute_query(sql, (company_id,))[0]
        # company_login_passwordの文字数を取得して、*をかける
        new_company_login_password_length = len(new_company_login_password)
        hidden_new_company_login_password = "*" * new_company_login_password_length
        return {
            "company_id": data[0],
            "company_name": data[1],
            "company_email": data[2],
            "company_login_password": hidden_new_company_login_password
        }

    def add_employee(self, company_id, employee_name, employee_email, authority):
        # 社員を追加する
        # add: ハッシュ化したパスワードをデータベースに保存する
        # add: sessionにemployee_idを保存する
        # add: tmp_employee_login_passwordを隠して通信する
        tmp_employee_login_password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        sql = "INSERT INTO employees (company_id, employee_name, employee_email, authority, employee_login_password)\
            VALUES (%s, %s, %s, %s, %s)"
        self.execute_query(sql, (company_id, employee_name, employee_email, authority, tmp_employee_login_password))

        # 社員IDを取得する
        sql = "SELECT employee_id, employee_name, employee_email, authority, employee_login_password\
            FROM employees\
            WHERE company_id = %s AND employee_email = %s"
        data = self.execute_query(sql, (company_id, employee_email))[0]
        return {
            "employee_id": data[0],
            "employee_name": data[1],
            "employee_email": data[2],
            "authority": data[3],
            "employee_login_password": tmp_employee_login_password,
        }

    def get_employees(self, company_id, authority):
        # 全社員情報を取得する
        # もしauthorityがNoneでなければ、その権限の社員のみ取得する
        sql = "SELECT employee_id, employee_name, employee_email, authority FROM employees WHERE company_id = %s"
        values = (company_id,)
        if authority:
            sql += " AND authority = %s"
            values += (authority,)
        data = self.execute_query(sql, values)

        employees = [
            {
                "employee_id": employee[0],
                "employee_name": employee[1],
                "employee_email": employee[2],
                "authority": employee[3],
            }
            for employee in data
        ]

        return {
            "employees": employees,
        }

    def delete_employee(self, company_id, employee_id):
        # 社員を削除する
        sql = "DELETE FROM employees WHERE company_id = %s AND employee_id = %s"
        self.execute_query(sql, (company_id, employee_id))

        return {
            "employee_id": employee_id,
        }

    def download_monthly_work_records(self, company_id, employee_id, year, month):
        # 月別勤怠情報をダウンロードする
        # add: csvで返す。https://dajiro.com/entry/2021/04/03/230945
        return {
            "employee_id": employee_id,
            "year": year,
            "month": month,
            "work_records": "csv形式の勤怠情報を返します。"
        }

    def get_correction_requests(self, company_id, year, month):
        # 月ごとの修正依頼を取得する
        # 月ごとの修正依頼を取得する
        status = "REQUESTED"
        sql = "SELECT correction_record_id, employee_id, work_date, start_work_at, finish_work_at, start_break_at,\
                    finish_break_at, start_overwork_at, finish_overwork_at, workplace, work_contents\
                FROM correction_records\
                WHERE company_id = %s AND EXTRACT(YEAR FROM work_date) = %s AND EXTRACT(MONTH FROM work_date) = %s AND status = %s"
        data = self.execute_query(sql, (company_id, year, month, status))

        # add: day_of_the_weekとwork_statusを追加する
        correction_records = [
            {
                "correction_record_id": correction_record[0],
                "employee_id": correction_record[1],
                "work_date": correction_record[2],
                "start_work_at": correction_record[3],
                "finish_work_at": correction_record[4],
                "start_break_at": correction_record[5],
                "finish_break_at": correction_record[6],
                "start_overwork_at": correction_record[7],
                "finish_overwork_at": correction_record[8],
                "workplace": correction_record[9],
                "work_contents": correction_record[10],
            } for correction_record in data
        ]

        return {
            "year": year,
            "month": month,
            "correction_records": correction_records
        }

    def approve_correction(self, company_id, correction_record_id):
        # 修正依頼を承認する
        status = "APPROVED"
        confirmed_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "UPDATE correction_records\
                SET status = %s, confirmed_at = %s\
                WHERE company_id = %s AND correction_record_id = %s"
        self.execute_query(sql, (status, confirmed_at, company_id, correction_record_id))
        return {
            "status": status,
            "correction_record_id": correction_record_id,
        }

    def reject_correction(self, company_id, correction_record_id, reject_reason):
        # 修正依頼を却下する
        status = "REJECTED"
        confirmed_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "UPDATE correction_records\
                SET status = %s, confirmed_at = %s, reject_reason = %s\
                WHERE company_id = %s AND correction_record_id = %s"
        self.execute_query(sql, (status, confirmed_at, reject_reason, company_id, correction_record_id))
        return {
            "status": status,
            "correction_record_id": correction_record_id,
        }

    def get_paid_leaves_records(self, company_id, year, month):
        # 有給休暇申請を取得する
        sql = "SELECT paid_leave_record_id, employee_id, paid_leave_date,\
                    work_type, paid_leave_reason, requested_at, status\
                FROM paid_leaves_records\
                WHERE company_id = %s AND EXTRACT(YEAR FROM requested_at) = %s\
                    AND EXTRACT(MONTH FROM requested_at) = %s"
        data = self.execute_query(sql, (company_id, year, month))

        paid_leaves_records = [
            {
                "paid_leave_record_id": paid_leave_record[0],
                "employee_id": paid_leave_record[1],
                "paid_leave_date": paid_leave_record[2],
                "work_type": paid_leave_record[3],
                "paid_leave_reason": paid_leave_record[4],
                "requested_at": paid_leave_record[5],
                "status": paid_leave_record[6],
            }
            for paid_leave_record in data
        ]

        return {
            "paid_leaves_records": paid_leaves_records,
        }

    def get_paid_leaves_days(self, company_id, year):
        # 有給休暇日数の情報を取得する
        sql = "SELECT employee_id, max_paid_leave_days, used_paid_leave_days\
                FROM paid_leaves_days\
                WHERE company_id = %s AND year = %s"
        data = self.execute_query(sql, (company_id, year))

        paid_leaves_days = [
            {
                "employee_id": paid_leave_day[0],
                "max_paid_leave_days": paid_leave_day[1],
                "used_paid_leave_days": paid_leave_day[2],
                "remaining_paid_leave_days": paid_leave_day[1] - paid_leave_day[2],
            }
            for paid_leave_day in data
        ]

        return {
            "paid_leaves_days": paid_leaves_days,
        }

    def set_remaining_paid_leave_days(self, company_id, employee_id, year, max_paid_leaves_days):
        # もし(company_id, employee_id, year)の組み合わせが存在しないなら、新しく作成する
        sql = "SELECT employee_id , employee_id, year\
                FROM paid_leaves_days\
                WHERE company_id = %s AND employee_id = %s AND year = %s"
        data = self.execute_query(sql, (company_id, employee_id, year))
        if len(data) == 0:
            sql = "INSERT INTO paid_leaves_days\
                    (company_id, employee_id, year, max_paid_leave_days, used_paid_leave_days)\
                    VALUES (%s, %s, %s, %s, %s)"
            self.execute_query(sql, (company_id, employee_id, year, max_paid_leaves_days, 0))
        else:
            sql = "UPDATE paid_leaves_days\
                    SET max_paid_leave_days = %s, used_paid_leave_days = %s\
                    WHERE company_id = %s AND employee_id = %s AND year = %s"
            self.execute_query(sql, (max_paid_leaves_days, 0, company_id, employee_id, year))

        return {
            "employee_id": employee_id,
            "year": year,
            "max_paid_leaves_days": max_paid_leaves_days,
            "used_paid_leave_days": 0,
            "remaining_paid_leave_days": max_paid_leaves_days,
        }

    def approve_paid_leave(self, company_id, paid_leave_record_id):
        # 有給休暇申請を承認する
        # もしstatusがAPPROVEDなら、何もしない
        sql = "SELECT status FROM paid_leaves_records\
                WHERE company_id = %s AND paid_leave_record_id = %s"
        data = self.execute_query(sql, (company_id, paid_leave_record_id))
        if data[0][0] == "APPROVED" or data[0][0] == "REJECTED":
            return {
                "error": "すでに確認されています。"
            }

        # もしmax_paid_leave_days - used_paid_leave_daysを取得
        sql = "SELECT max_paid_leave_days - used_paid_leave_days\
                FROM paid_leaves_days\
                WHERE company_id = %s\
                    AND employee_id = (\
                        SELECT employee_id\
                        FROM paid_leaves_records\
                        WHERE company_id = %s AND paid_leave_record_id = %s)\
                    AND year = EXTRACT(YEAR FROM (\
                        SELECT paid_leave_date\
                        FROM paid_leaves_records\
                        WHERE company_id = %s AND paid_leave_record_id = %s))"
        data = self.execute_query(sql, (company_id, company_id, paid_leave_record_id, company_id, paid_leave_record_id))
        remaining_paid_leave_days = data[0][0]
        sql = "SELECT work_type FROM paid_leaves_records\
                WHERE company_id = %s AND paid_leave_record_id = %s"
        data = self.execute_query(sql, (company_id, paid_leave_record_id))
        work_type = data[0][0]
        if work_type == "ALL_DAYS_LEAVES":
            remaining_paid_leave_days -= 1
        elif work_type == "MORNING_LEAVE" or work_type == "AFTERNOON_LEAVE":
            remaining_paid_leave_days -= 0.5
        if remaining_paid_leave_days < 0:
            return {
                "error": "有給休暇日数が足りません。"
            }

        confirmed_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "UPDATE paid_leaves_records\
                SET status = %s, confirmed_at = %s\
                WHERE company_id = %s AND paid_leave_record_id = %s"
        self.execute_query(sql, ("APPROVED", confirmed_at, company_id, paid_leave_record_id))

        # ここで、残り有給休暇日数を減らす。
        # もしwork_typeがALL_DAYS_LEAVESなら、used_paid_leave_daysを1増やす
        # MORNING_LEAVE, AFTERNOON_LEAVEなら、used_paid_leave_daysを0.5増やす
        # paid_leaves_recordsからpaid_leave_dateの年を取得して、yearに入れる
        sql = "UPDATE paid_leaves_days\
                SET used_paid_leave_days = used_paid_leave_days +\
                    (SELECT CASE WHEN work_type = %s THEN 1\
                            WHEN work_type = %s THEN 0.5\
                            WHEN work_type = %s THEN 0.5\
                            ELSE 0 END\
                        FROM paid_leaves_records\
                        WHERE company_id = %s AND paid_leave_record_id = %s)\
                WHERE company_id = %s\
                    AND employee_id =(\
                        SELECT employee_id\
                        FROM paid_leaves_records\
                        WHERE company_id = %s AND paid_leave_record_id = %s)\
                    AND year = (\
                        SELECT EXTRACT(YEAR FROM paid_leave_date)\
                        FROM paid_leaves_records\
                        WHERE company_id = %s AND paid_leave_record_id = %s)"
        self.execute_query(sql, (
            "ALL_DAY_LEAVE", "MORNING_LEAVE", "AFTERNOON_LEAVE",
            company_id, paid_leave_record_id, company_id,
            company_id, paid_leave_record_id, company_id, paid_leave_record_id))

        return {
            "paid_leave_record_id": paid_leave_record_id,
        }

    def reject_paid_leave(self, company_id, paid_leave_record_id, reject_reason):
        # 有給休暇申請を却下する
        sql = "UPDATE paid_leaves_records\
                SET status = REJECTED, reject_reason = %s, confirmed_at = NOW()\
                WHERE company_id = %s AND paid_leave_record_id = %s"
        self.execute_query(sql, (reject_reason, company_id, paid_leave_record_id))

        return {
            "paid_leave_record_id": paid_leave_record_id,
        }

    ######################################################################################
    # 全員ができる操作
    ######################################################################################

    def get_token(self, company_id, employee_email, employee_login_password):
        # トークンを取得する
        # fix: パスワードを暗号化する
        pass

    def login(self, company_id, employee_email, employee_login_password):
        # ログインする
        # fix: パスワードを暗号化する
        # fix: セッションを作成する
        # add: メールアドレスが違う場合の処理を追加する
        sql = "SELECT employee_id, employee_name, employee_login_password\
                FROM employees\
                WHERE company_id = %s AND employee_email = %s"
        data = self.execute_query(sql, (company_id, employee_email))[0]
        # もし、メールアドレスが違うなら、空の辞書を返す
        if data is None:
            return {
                "company_id": "",
                "employee_id": "",
                "employee_email": "",
                "employee_name": "",
                "error": "company_id or mail address is wrong",
                "is_active": False
            }
        # もし、パスワードが違うなら、空の辞書を返す
        if data[2] != employee_login_password:
            return {
                "company_id": "",
                "employee_id": "",
                "employee_email": "",
                "employee_name": "",
                "error": "password is wrong",
                "is_active": False
            }

        return {
            "company_id": company_id,
            "employee_id": data[0],
            "employee_email": employee_email,
            "employee_name": data[1],
            "error": "",
            "is_active": True
        }

    def logout(self):
        # ログアウトする
        # add: セッションを破棄する
        return {
            "is_active": False
        }

    def get_my_information(self, company_id, employee_id):
        # 社員情報を取得する
        sql = "SELECT company_id, employee_id, employee_name, employee_email, authority, commuting_expenses FROM employees WHERE company_id = %s AND employee_id = %s"
        data = self.execute_query(sql, (company_id, employee_id))[0]

        return {
            "company_id": data[0],
            "employee_id": data[1],
            "employee_name": data[2],
            "employee_email": data[3],
            "authority": data[4],
            "commuting_expenses": data[5]
        }

    def update_my_information(self, company_id, employee_id, employee_name, employee_email, old_employee_login_password, new_employee_login_password, commuting_expenses):
        # 社員情報を更新する
        # add: old_employee_login_passwordをハッシュ化してデータベースに保存されている内容と一致するかどうかを確認する
        # add: new_employee_login_passwordを**で隠して、文字数だけ返す

        sql = "SELECT employee_login_password FROM employees WHERE company_id = %s AND employee_id = %s"
        employee_login_password = self.execute_query(sql, (company_id, employee_id))[0][0]
        if employee_login_password != old_employee_login_password:
            return {
                "error": "パスワードが間違っています",
            }
        # 空じゃないものだけ更新する
        if employee_name != "":
            sql = "UPDATE employees SET employee_name = %s WHERE company_id = %s AND employee_id = %s"
            self.execute_query(sql, (employee_name, company_id, employee_id))
        if employee_email != "":
            sql = "UPDATE employees SET employee_email = %s WHERE company_id = %s AND employee_id = %s"
            self.execute_query(sql, (employee_email, company_id, employee_id))
        if new_employee_login_password != "":
            sql = "UPDATE employees SET employee_login_password = %s WHERE company_id = %s AND employee_id = %s"
            self.execute_query(sql, (new_employee_login_password, company_id, employee_id))
        if commuting_expenses != "":
            sql = "UPDATE employees SET commuting_expenses = %s WHERE company_id = %s AND employee_id = %s"
            self.execute_query(sql, (commuting_expenses, company_id, employee_id))
        # 従業員情報を取得する
        sql = "SELECT company_id, employee_id, employee_name, employee_email, commuting_expenses FROM employees WHERE company_id = %s AND employee_id = %s"
        data = self.execute_query(sql, (company_id, employee_id))[0]
        # employee_login_passwordの文字数を取得して、*をかける
        new_employee_login_password_length = len(new_employee_login_password)
        hidden_new_employee_login_password = "*" * new_employee_login_password_length
        return {
            "company_id": data[0],
            "employee_id": data[1],
            "employee_name": data[2],
            "employee_email": data[3],
            "employee_login_password": hidden_new_employee_login_password,
            "commuting_expenses": data[4],
        }

    def start_work_at(self, company_id, employee_id):
        # 労働開始ボタンを押す
        start_work_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        work_date = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = "INSERT INTO work_records (company_id, employee_id, work_date, start_work_at) VALUES (%s, %s, %s, %s)"
        self.execute_query(sql, (company_id, employee_id, work_date, start_work_at))

        return {
            "is_working": True,
            "work_date": work_date,
            "start_work_at": start_work_at
        }

    def finish_work_at(self, company_id, employee_id):
        # 労働終了ボタンを押す
        finish_work_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        work_date = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = "UPDATE work_records SET finish_work_at = %s WHERE company_id = %s AND employee_id = %s AND work_date = %s"
        self.execute_query(sql, (finish_work_at, company_id, employee_id, work_date))

        return {
            "is_working": False,
            "work_date": work_date,
            "finish_work_at": finish_work_at
        }

    def start_break_at(self, company_id, employee_id):
        # 休憩開始ボタンを押す
        start_break_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        work_date = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = "UPDATE work_records SET start_break_at = %s WHERE company_id = %s AND employee_id = %s AND work_date = %s"
        self.execute_query(sql, (start_break_at, company_id, employee_id, work_date))

        return {
            "is_working": False,
            "work_date": work_date,
            "start_break_at": start_break_at
        }

    def finish_break_at(self, company_id, employee_id):
        # 休憩終了ボタンを押す
        finish_break_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        work_date = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = "UPDATE work_records SET finish_break_at = %s WHERE company_id = %s AND employee_id = %s AND work_date = %s"
        self.execute_query(sql, (finish_break_at, company_id, employee_id, work_date))

        return {
            "is_working": True,
            "work_date": work_date,
            "finish_break_at": finish_break_at
        }

    def start_overwork_at(self, company_id, employee_id):
        # 残業開始ボタンを押す
        start_overwork_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        work_date = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = "UPDATE work_records SET start_overwork_at = %s WHERE company_id = %s AND employee_id = %s AND work_date = %s"
        self.execute_query(sql, (start_overwork_at, company_id, employee_id, work_date))

        return {
            "is_working": True,
            "work_date": work_date,
            "start_overwork_at": start_overwork_at
        }

    def finish_overwork_at(self, company_id, employee_id):
        # 残業終了ボタンを押す
        finish_overwork_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        work_date = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = "UPDATE work_records SET finish_overwork_at = %s WHERE company_id = %s AND employee_id = %s AND work_date = %s"
        self.execute_query(sql, (finish_overwork_at, company_id, employee_id, work_date))

        return {
            "is_working": False,
            "work_date": work_date,
            "finish_overtime_work_at": finish_overwork_at
        }

    def work_contents(self, company_id, employee_id, work_record_id, workplace, work_contents):
        # 作業内容を記録する
        sql = "UPDATE work_records SET workplace = %s, work_contents = %s WHERE company_id = %s AND employee_id = %s AND work_record_id = %s"
        self.execute_query(sql, (workplace, work_contents, company_id, employee_id, work_record_id))
        return {
            "work_record_id": work_record_id,
            "workplace": workplace,
            "work_contents": work_contents
        }

    def get_monthly_work_records(self, company_id, employee_id, year, month):
        # 月別勤怠情報を取得する
        # fix: calendarとpaid_leavesを結合し、それとwork_recordsを結合する
        # fix: work_dateはpaid_leavesから取得する
        # fix: 結合したものからemployee_id, year, monthで絞り込み、work_dateでソートする
        # add: day_of_the_weekとwork_statusを追加する
        sql = """
            SELECT
                calendar.date,
                calendar.day_of_the_week,
                paid_leaves.work_status,
                work_records.start_work_at,
                work_records.finish_work_at,
                work_records.start_break_at,
                work_records.finish_break_at,
                work_records.start_overwork_at,
                work_records.finish_overwork_at,
                work_records.workplace,
                work_records.work_contents
            FROM calendar
            LEFT JOIN paid_leaves
                ON calendar.date = paid_leaves.date AND
                    calendar.company_id = paid_leaves.company_id AND
                    paid_leaves.employee_id = %s
            LEFT JOIN work_records
                ON calendar.date = work_records.work_date AND
                    calendar.company_id = work_records.company_id AND
                    paid_leaves.employee_id = work_records.employee_id
            WHERE
                work_records.company_id = %s AND
                work_records.employee_id = %s AND
                YEAR(work_records.work_date) = %s AND
                MONTH(work_records.work_date) = %s
            ORDER BY calendar.date
        """
        data = self.execute_query(sql, (employee_id, company_id, employee_id, year, month))
        work_records = [
            {
                "work_date": work_record[0],
                "start_work_at": work_record[1],
                "finish_work_at": work_record[2],
                "start_break_at": work_record[3],
                "finish_break_at": work_record[4],
                "start_overtime_work_at": work_record[5],
                "finish_overtime_work_at": work_record[6],
                "workplace": work_record[7],
                "work_contents": work_record[8]
            } for work_record in data
        ]

        return {
            "year": year,
            "month": month,
            "work_records": work_records
        }

    def request_correction(self, company_id, employee_id, work_date, start_work_at, finish_work_at, start_break_at, finish_break_at, start_overtime_work_at, finish_overtime_work_at, workplace, work_contents):
        # 修正依頼をする
        sql = "INSERT INTO correction_records (\
                company_id, employee_id, work_date, "
        variables = [company_id, employee_id, work_date]
        values = "VALUES (%s, %s, %s, "
        if start_work_at != "":
            # sqlの最後にstart_work_atを追加する
            sql += "start_work_at,"
            values += "%s,"
            variables.append(start_work_at)
        if finish_work_at != "":
            sql += "finish_work_at,"
            values += "%s,"
            variables.append(finish_work_at)
        if start_break_at != "":
            sql += "start_break_at,"
            values += "%s,"
            variables.append(start_break_at)
        if finish_break_at != "":
            sql += "finish_break_at,"
            values += "%s,"
            variables.append(finish_break_at)
        if start_overtime_work_at != "":
            sql += "start_overwork_at,"
            values += "%s,"
            variables.append(start_overtime_work_at)
        if finish_overtime_work_at != "":
            sql += "finish_overwork_at,"
            values += "%s,"
            variables.append(finish_overtime_work_at)
        if workplace != "":
            sql += "workplace,"
            values += "%s,"
            variables.append(workplace)
        if work_contents != "":
            sql += "work_contents,"
            values += "%s,"
            variables.append(work_contents)
        sql += "status, confirmed_at, reject_reason) "
        values += "%s, %s, %s)"
        variables.append("REQUESTED")
        variables.append(None)
        variables.append(None)
        sql += values
        self.execute_query(sql, variables)

        return {
            "work_date": work_date,
            "start_work_at": start_work_at,
            "finish_work_at": finish_work_at,
            "start_break_at": start_break_at,
            "finish_break_at": finish_break_at,
            "start_overtime_work_at": start_overtime_work_at,
            "finish_overtime_work_at": finish_overtime_work_at,
            "workplace": workplace,
            "work_contents": work_contents
        }

    def request_paid_leave(self, company_id, employee_id, paid_leave_date, work_type, paid_leave_reason):
        # 有給休暇申請をする
        # もし、max_paid_leave_days-used_paid_leave_daysが0の場合、エラーを返す
        sql = "SELECT max_paid_leave_days, used_paid_leave_days FROM paid_leaves_days WHERE company_id = %s AND employee_id = %s"
        data = self.execute_query(sql, (company_id, employee_id))
        max_paid_leave_days = data[0][0]
        used_paid_leave_days = data[0][1]
        if max_paid_leave_days - used_paid_leave_days == 0:
            return {
                "error": "有休がありません。"
            }

        requested_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO paid_leaves_records (\
                company_id, employee_id, paid_leave_date,\
                work_type, paid_leave_reason,\
                requested_at, status,\
                confirmed_at, reject_reason)\
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.execute_query(sql, (company_id, employee_id, paid_leave_date, work_type, paid_leave_reason, requested_at, "REQUESTED", None, None))

        return {
            "paid_leave_date": paid_leave_date,
            "work_type": work_type,
            "requested_at": requested_at,
            "paid_leave_reason": paid_leave_reason
        }

    def get_my_paid_leaves_records(self, company_id, employee_id, year, month):
        # 月ごと有給休暇申請を取得する
        sql = "SELECT paid_leave_record_id, paid_leave_date, work_type, paid_leave_reason,\
                    requested_at, status, confirmed_at, reject_reason\
                FROM paid_leaves_records\
                WHERE company_id = %s AND employee_id = %s AND EXTRACT(YEAR FROM paid_leave_date) = %s AND EXTRACT(MONTH FROM paid_leave_date) = %s"
        data = self.execute_query(sql, (company_id, employee_id, year, month))

        paid_leaves_records = [
            {
                "paid_leave_record_id": paid_leave_record[0],
                "paid_leave_date": paid_leave_record[1],
                "work_type": paid_leave_record[2],
                "paid_leave_reason": paid_leave_record[3],
                "requested_at": paid_leave_record[4],
                "status": paid_leave_record[5],
                "confirmed_at": paid_leave_record[6],
                "reject_reason": paid_leave_record[7],
            } for paid_leave_record in data
        ]

        return {
            "year": year,
            "month": month,
            "paid_leaves_records": paid_leaves_records
        }

    def get_my_paid_leave_days(self, company_id, employee_id, year):
        # 残り有給休暇日数を取得する
        sql = "SELECT max_paid_leave_days, used_paid_leave_days, max_paid_leave_days-used_paid_leave_days\
                FROM paid_leaves_days\
                WHERE company_id = %s AND employee_id = %s AND year = %s"
        data = self.execute_query(sql, (company_id, employee_id, year))

        paid_leave_days = [
            {
                "max_paid_leave_days": paid_leave_day[0],
                "used_paid_leave_days": paid_leave_day[1],
                "remaining_paid_leave_days": paid_leave_day[2]
            } for paid_leave_day in data
        ]

        return {
            "year": year,
            "paid_leave_days": paid_leave_days
        }
