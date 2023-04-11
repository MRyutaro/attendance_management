"""
emailもしくは会社idと従業員idで一意に識別できるようにする
パスワードはハッシュ化して保存する
"""

import datetime
import random
import string
import time

import psycopg2


class Models():
    def __init__(self):
        # postgresqlに接続する
        # fix: 環境変数から取得する
        MODE = "dev"
        if MODE == "dev":
            self.host = "localhost"
            self.port = 5432
            self.password = "1028"
            self.user = "postgres"
            self.database = "db"
        elif MODE == "prod":
            self.host = "db"
            self.port = 5432
            self.password = "password"
            self.user = "user"
            self.database = "db"
        # fix: 接続できるまで繰り返す
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
                sql = "CREATE TABLE IF NOT EXISTS companies (\
                company_id SERIAL PRIMARY KEY,\
                company_name VARCHAR(30),\
                company_email VARCHAR(30) UNIQUE,\
                company_login_password VARCHAR(30),\
                UNIQUE (company_id, company_email))"
                cursor.execute(sql)
            conn.commit()

    def create_other_tables(self):
        # テーブルを作成する
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # day_of_the_weekのenumを作成
                sql = "CREATE TYPE DAY_OF_THE_WEEK AS ENUM ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # work_statusのenumを作成
                sql = "CREATE TYPE WORK_TYPE AS ENUM ('DAY_OFF', 'WORKDAY', 'HOLIDAY', 'ALL_DAY_LEAVES', 'MORNING_LEAVES', 'AFTERNOON_LEAVES')"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # workpalceのenumを作成
                sql = "CREATE TYPE WORKPLACE AS ENUM ('OFFICE', 'HOME', 'OTHER')"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # statusのenumを作成
                sql = "CREATE TYPE STATUS AS ENUM ('REQUESTED', 'APPROVED', 'REJECTED')"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # authorityのenumを作成
                sql = "CREATE TYPE AUTHORITY AS ENUM ('ADMIN', 'USER')"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # カレンダーテーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS calendar (\
                        company_id INTEGER,\
                        date TIMESTAMP,\
                        day_of_the_week DAY_OF_THE_WEEK,\
                        work_type WORK_TYPE,\
                        PRIMARY KEY (company_id, date),\
                        FOREIGN KEY (company_id) REFERENCES companies(company_id))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 従業員テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS employees (\
                        company_id INTEGER,\
                        employee_id SERIAL,\
                        employee_name VARCHAR(30),\
                        employee_email VARCHAR(30),\
                        employee_login_password VARCHAR(30),\
                        authority AUTHORITY,\
                        commuting_expenses INTEGER,\
                        UNIQUE (company_id, employee_id),\
                        UNIQUE (company_id, employee_email),\
                        FOREIGN KEY (company_id) REFERENCES companies(company_id))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 勤怠記録テーブルを作成
                # delete: work_record_idはいらないかも
                sql = "CREATE TABLE IF NOT EXISTS work_records (\
                        work_record_id SERIAL PRIMARY KEY,\
                        company_id INTEGER,\
                        employee_id INTEGER,\
                        work_date DATE,\
                        start_work_at TIME,\
                        finish_work_at TIME,\
                        start_break_at TIME,\
                        finish_break_at TIME,\
                        start_overwork_at TIME,\
                        finish_overwork_at TIME,\
                        workplace WORKPLACE,\
                        work_contents VARCHAR(50),\
                        UNIQUE (company_id, employee_id, work_date),\
                        FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 勤怠修正記録テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS correction_records (\
                        correction_record_id SERIAL PRIMARY KEY,\
                        company_id INTEGER,\
                        employee_id INTEGER,\
                        work_date TIMESTAMP,\
                        start_work_at TIME,\
                        finish_work_at TIME,\
                        start_break_at TIME,\
                        finish_break_at TIME,\
                        start_overwork_at TIME,\
                        finish_overwork_at TIME,\
                        workplace WORKPLACE,\
                        work_contents VARCHAR(50),\
                        status STATUS,\
                        confirmed_at TIMESTAMP,\
                        reject_reason VARCHAR(50),\
                        UNIQUE (company_id, correction_record_id),\
                        FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 有休カレンダーテーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS work_calendars (\
                        company_id INTEGER,\
                        employee_id INTEGER,\
                        date DATE,\
                        work_type WORK_TYPE,\
                        UNIQUE (company_id, employee_id, date),\
                        FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id))"
            conn.commit()
            with conn.cursor() as cursor:
                # 有休申請記録テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS paid_leaves_records (\
                        paid_leave_id SERIAL PRIMARY KEY,\
                        company_id INTEGER,\
                        employee_id INTEGER,\
                        paid_leave_date DATE,\
                        work_type WORK_TYPE,\
                        requested_at TIMESTAMP,\
                        status STATUS,\
                        confirmed_at TIMESTAMP,\
                        reject_reason VARCHAR(50),\
                        UNIQUE (company_id, paid_leave_id),\
                        FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 有休日数テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS paid_leaves_days (\
                        company_id INTEGER,\
                        employee_id INTEGER,\
                        year INTEGER,\
                        max_paid_leaves_days FLOAT,\
                        used_paid_leaves_days FLOAT,\
                        UNIQUE (company_id, employee_id, year),\
                        FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id))"
                cursor.execute(sql)
            conn.commit()

    ######################################################################################
    # ここから管理者用
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

    def get_employees(self, company_id):
        # 全社員情報を取得する
        sql = "SELECT employee_id, employee_name, employee_email, authority FROM employees WHERE company_id = %s"
        data = self.execute_query(sql, (company_id,))

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
        sql = "SELECT correction_record_id, employee_id, work_date, start_work_at, finish_work_at,\
                start_break_at, finish_break_at, start_overtime_work_at, finish_overtime_work_at, workplace, work_content,\
                FROM correction_records\
                WHERE company_id = %s AND EXTRACT(YEAR FROM work_date) = %s\
                    AND EXTRACT(MONTH FROM work_date) = %s AND status = REQUESTED"
        data = self.execute_query(sql, (company_id, year, month))

        correction_requests = [
            {
                "correction_record_id": correction_request[0],
                "employee_id": correction_request[1],
                "work_date": correction_request[2],
                "start_work_at": correction_request[3],
                "finish_work_at": correction_request[4],
                "start_break_at": correction_request[5],
                "finish_break_at": correction_request[6],
                "start_overtime_work_at": correction_request[7],
                "finish_overtime_work_at": correction_request[8],
                "workplace": correction_request[9],
                "work_content": correction_request[10],
            }
            for correction_request in data
        ]

        return {
            "correction_requests": correction_requests,
        }

    def approve_correction(self, company_id, correction_record_id):
        # 修正依頼を承認する
        sql = "UPDATE correction_records\
                SET status = APPROVED, comfirmed_at = NOW()\
                WHERE company_id = %s AND correction_record_id = %s"
        self.execute_query(sql, (company_id, correction_record_id))
        return {
            "correction_record_id": correction_record_id,
        }

    def reject_correction(self, company_id, correction_record_id, reject_reason):
        # 修正依頼を却下する
        sql = "UPDATE correction_records\
                SET status = REJECTED, comfirmed_at = NOW(), reject_reason = %s\
                WHERE company_id = %s AND correction_record_id = %s"
        self.execute_query(sql, (reject_reason, company_id, correction_record_id))
        return {
            "correction_record_id": correction_record_id,
        }

    def get_paid_leaves_records(self, company_id, year, month):
        # 有給休暇申請を取得する
        sql = "SELECT paid_leaves_record_id, employee_id, paid_leave_date, work_type, paid_leaves_reason,\
                requested_at\
                FROM paid_leaves_records\
                WHERE company_id = %s AND EXTRACT(YEAR FROM requested_at) = %s\
                    AND EXTRACT(MONTH FROM requested_at) = %s AND status = REQUESTED"
        data = self.execute_query(sql, (company_id, year, month))

        paid_leaves_records = [
            {
                "paid_leaves_record_id": paid_leaves_record[0],
                "employee_id": paid_leaves_record[1],
                "paid_leave_date": paid_leaves_record[2],
                "work_type": paid_leaves_record[3],
                "paid_leaves_reason": paid_leaves_record[4],
                "requested_at": paid_leaves_record[5],
            }
            for paid_leaves_record in data
        ]

        return {
            "paid_leaves_records": paid_leaves_records,
        }

    def get_paid_leaves_days(self, company_id, year):
        # 有給休暇日数の情報を取得する
        sql = "SELECT employee_id, max_paid_leaves_days, used_paid_leaves_days\
                FROM paid_leaves_days\
                WHERE company_id = %s AND EXTRACT(YEAR FROM year) = %s"
        data = self.execute_query(sql, (company_id, year))

        paid_leaves_days = [
            {
                "employee_id": paid_leaves_day[0],
                "max_paid_leaves_days": paid_leaves_day[1],
                "used_paid_leaves_days": paid_leaves_day[2],
                "remaining_paid_leaves_days": paid_leaves_day[1] - paid_leaves_day[2],
            }
            for paid_leaves_day in data
        ]

        return {
            "paid_leaves_days": paid_leaves_days,
        }

    def set_remaining_paid_leaves_days(self, company_id, employee_id, year, max_paid_leaves_days):
        # 残り有給休暇日数を設定する
        # 一気に設定する
        sql = "INSERT INTO paid_leaves_days (\
                company_id, employee_id, year, max_paid_leaves_days, used_paid_leaves_days)\
                VALUES (%s, %s, %s, %s, 0)"
        self.execute_query(sql, (company_id, employee_id, year, max_paid_leaves_days))

        return {
            "employee_id": employee_id,
            "year": year,
            "max_paid_leaves_days": max_paid_leaves_days,
            "used_paid_leaves_days": 0,
            "remaining_paid_leaves_days": max_paid_leaves_days,
        }

    def approve_paid_leave(self, company_id, paid_leave_record_id):
        # 有給休暇申請を承認する
        sql = "UPDATE paid_leaves_records\
                SET status = APPROVED, comfirmed_at = NOW()\
                WHERE company_id = %s AND paid_leaves_record_id = %s"
        self.execute_query(sql, (company_id, paid_leave_record_id))

        # ここで、残り有給休暇日数を減らす。
        # もしwork_typeがALL_DAYS_LEAVESなら、used_paid_leaves_daysを1増やす
        # MORNING_LEAVES, AFTERNOON_LEAVESなら、used_paid_leaves_daysを0.5増やす
        # paid_leaves_recordsからpaid_leave_dateの年を取得して、yearに入れる
        sql = "UPDATE paid_leaves_days\
                SET used_paid_leaves_days = used_paid_leaves_days +\
                    (SELECT CASE WHEN work_type = 'ALL_DAYS_LEAVES' THEN 1\
                            WHEN work_type = 'MORNING_LEAVES' THEN 0.5\
                            WHEN work_type = 'AFTERNOON_LEAVES' THEN 0.5\
                            ELSE 0 END\
                        FROM paid_leaves_records\
                        WHERE company_id = %s AND paid_leaves_record_id = %s)\
                WHERE company_id = %s AND employee_id = %s AND\
                    year = (SELECT EXTRACT(YEAR FROM paid_leave_date)\
                        FROM paid_leaves_records\
                        WHERE company_id = %s AND paid_leaves_record_id = %s)"
        self.execute_query(sql, (company_id, paid_leave_record_id, company_id, paid_leave_record_id))

        return {
            "paid_leave_record_id": paid_leave_record_id,
        }

    def reject_paid_leave(self, company_id, paid_leave_record_id, reject_reason):
        # 有給休暇申請を却下する
        sql = "UPDATE paid_leaves_records\
                SET status = REJECTED, reject_reason = %s, comfirmed_at = NOW()\
                WHERE company_id = %s AND paid_leaves_record_id = %s"
        self.execute_query(sql, (reject_reason, company_id, paid_leave_record_id))

        return {
            "paid_leave_record_id": paid_leave_record_id,
        }

    ######################################################################################
    # 従業員ができる操作
    ######################################################################################

    def login(self, company_id, employee_email, employee_login_password):
        # ログインする
        # fix: パスワードを暗号化する
        # fix: セッションを作成する
        # add: メールアドレスが違う場合の処理を追加する
        sql = "SELECT employee_id, employee_name, employee_login_password\
                FROM employees\
                WHERE company_id = %s AND employee_email = %s"
        data = self.execute_query(sql, (company_id, employee_email))[0]
        # もし、パスワードが違うなら、空の辞書を返す
        if data[2] != employee_login_password:
            return {
                "company_id": "",
                "employee_id": "",
                "employee_email": "",
                "employee_name": "",
                "error": "パスワードが違います",
                "is_active": False
            }

        return {
            "company_id": company_id,
            "employee_id": data[0],
            "employee_email": employee_email,
            "employee_name": data[1],
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
        sql = "SELECT work_date, start_work_at, finish_work_at, start_break_at,\
                    finish_break_at, start_overwork_at, finish_overwork_at, workplace, work_contents\
                FROM work_records\
                WHERE company_id = %s AND employee_id = %s AND EXTRACT(YEAR FROM work_date) = %s AND EXTRACT(MONTH FROM work_date) = %s"
        data = self.execute_query(sql, (company_id, employee_id, year, month))

        # add: day_of_the_weekとwork_statusを追加する
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
                company_id, employee_id, work_date, start_work_at, finish_work_at, start_break_at,\
                finish_break_at, start_overwork_at, finish_overwork_at, workplace,\
                work_contents, status, confirmed_at, reject_reason)\
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.execute_query(sql, (company_id, employee_id, work_date, start_work_at, finish_work_at, start_break_at, finish_break_at, start_overtime_work_at, finish_overtime_work_at, workplace, work_contents, "REQUESTED", None, None))

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

    def get_request_correction(self, company_id, employee_id, year, month):
        # 月ごとの修正依頼を取得する
        return {
            "year": year,
            "month": month,
            "correction_requests": [
                {
                    "correction_date": "2020-01-15",
                    "correction_contents": "出勤時間が9時ではなく10時でした。",
                    "is_approved": True,
                    "approved_at": "2020-01-16 09:00:00"
                },
                {
                    "correction_date": "2020-01-16",
                    "correction_contents": "出勤時間が9時ではなく10時でした。",
                    "is_approved": False,
                    "rejected_at": "2020-01-16 09:00:00",
                    "rejected_reason": "出勤時間が10時であることが確認できませんでした。"
                },
                {
                    "correction_date": "2020-01-16",
                    "correction_contents": "出勤時間が9時ではなく10時でした。",
                    "is_approved": None
                }
            ]
        }

    def request_paid_leave(self, company_id, employee_id, start_paid_leave_at, finish_paid_leave_at):
        # 有給休暇申請をする
        # fix: ここは時間指定じゃなくて日付指定+全休or半休でいいかも
        return {
            "start_paid_leave_at": start_paid_leave_at,
            "finish_paid_leave_at": finish_paid_leave_at,
            "paid_leave_reason": "病気のため"
        }

    def get_my_paid_leaves_records(self, company_id, employee_id, year, month):
        # 月ごと有給休暇申請を取得する
        return {
            "paid_leaves_records": [
                {
                    "start_paid_leave_at": "2020-01-01 09:00:00",
                    "finish_paid_leave_at": "2020-01-01 18:00:00",
                    "is_approved": True,
                    "approved_at": "2020-01-02 09:00:00"
                },
                {
                    "start_paid_leave_at": "2020-01-02 09:00:00",
                    "finish_paid_leave_at": "2020-01-02 18:00:00",
                    "is_approved": False,
                    "rejected_at": "2020-01-02 09:00:00",
                    "rejected_reason": "有給休暇の残日数が不足しています。"
                }
            ]
        }

    def get_my_remaining_paid_leaves_days(self, company_id, employee_id):
        # 残り有給休暇日数を取得する
        return {
            "remaining_paid_leaves_days": 10
        }
