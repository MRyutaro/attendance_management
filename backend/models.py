"""
emailもしくは会社idと従業員idで一意に識別できるようにする
パスワードはハッシュ化して保存する
"""

import random
import string
import time

import psycopg2


class Models():
    def __init__(self):
        # postgresqlに接続する
        # fix: 環境変数から取得する
        MODE = "prod"
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
                company_id SERIAL PRIMARY KEY, company_name VARCHAR(30),\
                company_email VARCHAR(30) UNIQUE, company_login_password VARCHAR(30),\
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
                sql = "CREATE TYPE WORK_STATUS AS ENUM ('DAY_OFF', 'WORKDAY', 'HOLIDAY', 'PAID_LEAVE')"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # workpalceのenumを作成
                sql = "CREATE TYPE WORKPLACE AS ENUM ('OFFICE', 'HOME', 'OTHER')"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # paid_leaves_typeのenumを作成
                sql = "CREATE TYPE PAID_LEAVES_TYPE AS ENUM ('ALL_DAY', 'MORNING', 'AFTERNOON')"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # statusのenumを作成
                sql = "CREATE TYPE STATUS AS ENUM ('REQUESTED', 'CONFIRMED', 'REJECTED')"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # authorityのenumを作成
                sql = "CREATE TYPE AUTHORITY AS ENUM ('ADMIN', 'USER')"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # カレンダーテーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS calendars (\
                company_id INTEGER,\
                FOREIGN KEY (company_id) REFERENCES companies(company_id),\
                date TIMESTAMP, day_of_the_week DAY_OF_THE_WEEK,\
                work_status WORK_STATUS,\
                PRIMARY KEY (company_id, date))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 従業員テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS employees (\
                employee_id SERIAL, company_id INTEGER,\
                FOREIGN KEY (company_id) REFERENCES companies(company_id),\
                employee_name VARCHAR(30), employee_email VARCHAR(30),\
                authority AUTHORITY, employee_login_password VARCHAR(30),\
                PRIMARY KEY (company_id, employee_id))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 勤怠記録テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS work_records (\
                work_record_id SERIAL PRIMARY KEY,\
                company_id INTEGER, employee_id INTEGER,\
                FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id),\
                work_date TIMESTAMP, day_of_the_week DAY_OF_THE_WEEK, work_status WORK_STATUS,\
                start_work_at TIME, finish_work_at TIME, start_break_at TIME, finish_break_at TIME,\
                start_overwork_at TIME, finish_overwork_at TIME,\
                workplace WORKPLACE, work_contents VARCHAR(50))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 勤怠修正依頼テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS correction_requests (\
                    correction_id SERIAL PRIMARY KEY,\
                    company_id INTEGER, employee_id INTEGER,\
                    FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id),\
                    correction_date TIMESTAMP, correction_contents VARCHAR(50),\
                    request_date TIMESTAMP, status STATUS,\
                    confirmed_at TIMESTAMP, reject_reason VARCHAR(50))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 有休記録テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS paid_leaves_recodes (\
                    paid_leave_id SERIAL PRIMARY KEY,\
                    company_id INTEGER, employee_id INTEGER,\
                    FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id),\
                    paid_leave_date TIMESTAMP, paid_leaves_type PAID_LEAVES_TYPE,\
                    request_date TIMESTAMP, status STATUS,\
                    confirmed_at TIMESTAMP, reject_reason VARCHAR(50))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 有休日数テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS paid_leaves_days (\
                company_id INTEGER, employee_id INTEGER,\
                FOREIGN KEY (company_id, employee_id) REFERENCES employees(company_id, employee_id),\
                year INTEGER, max_paid_leaves_days INTEGER,\
                used_paid_leaves_days INTEGER, remaining_paid_leaves_days INTEGER)"
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
        sql = "SELECT company_id, company_name, company_email, company_login_password FROM companies WHERE company_name = %s AND company_email = %s"
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
                "error": "古いパスワードが間違っています",
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
        tmp_employee_login_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        sql = "INSERT INTO employees (company_id, employee_name, employee_email, authority, employee_login_password) VALUES (%s, %s, %s, %s, %s)"
        self.execute_query(sql, (company_id, employee_name, employee_email, authority, tmp_employee_login_password))

        # 社員IDを取得する
        sql = "SELECT employee_id, employee_name, employee_email, authority, employee_login_password FROM employees WHERE company_id = %s AND employee_email = %s"
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
        return {
            "employees": [
                {
                    "employee_id": 1,
                    "employee_name": "山田太郎",
                    "employee_email": "aaa.com",
                },
                {
                    "employee_id": 2,
                    "employee_name": "鈴木花子",
                    "employee_email": "bbb.com",
                },
            ]
        }

    def delete_employee(self, company_id, employee_id):
        # 社員を削除する
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
            "work_records": "csv形式の勤怠情報"
        }

    def get_correction_requests(self, company_id, year, month):
        # 月ごとの修正依頼を取得する
        '''
        SELECT *
        FROM correction_records
        WHERE EXTRACT(YEAR FROM correction_request_date) = 2022;
        '''
        return {
            "year": year,
            "month": month,
            "correction_requests": [
                {
                    "correction_id": 1,
                    "employee_name": "山田太郎",
                    "correction_date": "2021-04-01",
                    "correction_contents": "出勤時間が9時ではなく10時でした。",
                },
                {
                    "correction_id": 2,
                    "employee_name": "鈴木花子",
                    "correction_date": "2021-04-01",
                    "correction_contents": "出勤時間が9時ではなく10時でした。",
                },
            ]
        }

    def approve_correction(self, company_id, correction_id):
        # 修正依頼を承認する
        return {
            "correction_id": correction_id,
            "correction_date": "2021-04-01",
            "correction_contents": "出勤時間が9時ではなく10時でした。",
        }

    def update_work_records(self, company_id, year, month, start_work_at, finish_work_at, start_break_at, finish_break_at, start_overtime_work_at, finish_overtime_work_at, workplace, work_content):
        # 勤怠情報を更新する
        # 修正しない場合は、Noneを入れる
        return {
            "employee_id": 1,
            "year": year,
            "month": month,
            "updated_contents": {
                "start_work_at": start_work_at,
                "finish_work_at": finish_work_at,
                "start_break_at": start_break_at,
                "finish_break_at": finish_break_at,
                "start_overtime_work_at": start_overtime_work_at,
                "finish_overtime_work_at": finish_overtime_work_at,
                "workplace": workplace,
                "work_content": work_content
            }
        }

    def reject_correction(self, company_id, year, month, correction_id, reject_reason):
        # 修正依頼を却下する
        # add: is_approvedをFalseにする
        # add: reject_reasonを入力する
        return {
            "employee_name": "山田太郎",
            "correction_date": "2021-04-01",
            "correction_contents": "出勤時間が9時ではなく10時でした。",
            "is_approved": False,
            "rejected_at": "2021-04-01 10:00:00",
            "reject_reason": reject_reason,
        }

    def get_paid_leaves_records(self, company_id, year, month):
        # 有給休暇申請を取得する
        return {
            "paid_leaves_records": [
                {
                    "employee_name": "山田太郎",
                    "paid_leave_date": "2021-04-01",
                    "paid_leave_reason": "病気",
                    "is_approved": True,
                    "approved_at": "2021-04-01 10:00:00",
                },
                {
                    "employee_name": "鈴木花子",
                    "paid_leave_date": "2021-04-01",
                    "paid_leave_reason": "病気",
                    "is_approved": False,
                    "rejected_at": "2021-04-01 10:00:00",
                    "reject_reason": "病気ではない",
                }
            ]
        }

    def get_remaining_paid_leaves_days(self, company_id):
        # 残り有給休暇日数を取得する
        return {
            "remaining_paid_leaves_days": [
                {
                    "employee_name": "山田太郎",
                    "remaining_paid_leaves_days": 10,
                },
                {
                    "employee_name": "鈴木花子",
                    "remaining_paid_leaves_days": 10,
                }
            ]
        }

    def set_remaining_paid_leaves_days(self, company_id, remaining_paid_leaves_days):
        # 残り有給休暇日数を設定する
        # 一気に設定する
        return {
            "remaining_paid_leaves_days": [
                {
                    "employee_name": "山田太郎",
                    "remaining_paid_leaves_days": remaining_paid_leaves_days,
                },
                {
                    "employee_name": "鈴木花子",
                    "remaining_paid_leaves_days": remaining_paid_leaves_days,
                }
            ]
        }

    def approve_paid_leave(self, company_id, paid_leave_record_id):
        # 有給休暇申請を承認する
        # ここで、残り有給休暇日数を減らす
        return {
            "start_paid_leave_at": "2021-04-01 9:00:00",
            "finish_paid_leave_at": "2021-04-01 12:00:00",
            "paid_leave_reason": "病気",
            "approved_at": "2021-04-01 10:00:00",
        }

    def reject_paid_leave(self, company_id, paid_leave_record_id, reject_reason):
        # 有給休暇申請を却下する
        return {
            "start_paid_leave_at": "2021-04-01 9:00:00",
            "finish_paid_leave_at": "2021-04-01 12:00:00",
            "paid_leave_reason": "病気",
            "rejected_at": "2021-04-01 10:00:00",
            "reject_reason": reject_reason,
        }

    ######################################################################################
    # memberができる操作
    ######################################################################################

    def signup(self, company_id, employee_id, employee_email, employee_name, employee_login_password):
        # 新規登録する
        # add: ハッシュ化したパスワードをデータベースに保存する
        # add: セッションで管理する
        # フローとしては、管理者が会社を登録→管理者が社員を登録→社員が登録する
        return {
            "employee_email": employee_email,
            "employee_name": employee_name,
            "is_active": True
        }

    def login(self, company_id, employee_id, employee_email, employee_login_password):
        # ログインする
        # add: データベースに保存されている内容と一致するかどうかを確認する
        # add: company_idとemployee_id, もしくはemployee_emailでログインできるように
        return {
            "company_id": company_id,
            "employee_id": employee_id,
            "employee_email": employee_email,
            "is_active": True
        }

    def logout(self):
        # ログアウトする
        # add: セッションを破棄する
        return {
            "is_active": False
        }

    def get_my_information(self, employee_email):
        # 社員情報を取得する
        return {
            "company_id": 1,
            "employee_id": 1,
            "employee_name": "山田太郎",
            "employee_email": employee_email,
            "authority": "member",
            "commuting_expenses": 1000
        }

    def update_my_information(self, employee_name, employee_email, old_employee_login_password, new_employee_login_password, commuting_expenses):
        # 社員情報を更新する
        # add: old_employee_login_passwordをハッシュ化してデータベースに保存されている内容と一致するかどうかを確認する
        # add: new_employee_login_passwordを**で隠して、文字数だけ返す
        return {
            "employee_name": employee_name,
            "employee_email": employee_email,
            "employee_login_password": "*******",
            "commuting_expenses": commuting_expenses
        }

    def start_work_at(self, company_id, employee_id, start_work_at):
        # 労働開始ボタンを押す
        return {
            "is_working": True,
            "start_work_at": start_work_at
        }

    def finish_work_at(self, company_id, employee_id, finish_work_at):
        # 労働終了ボタンを押す
        return {
            "is_working": False,
            "finish_work_at": finish_work_at
        }

    def start_break_at(self, company_id, employee_id, start_break_at):
        # 休憩開始ボタンを押す
        return {
            "is_working": False,
            "start_break_at": start_break_at
        }

    def finish_break_at(self, company_id, employee_id, finish_break_at):
        # 休憩終了ボタンを押す
        return {
            "is_working": True,
            "finish_break_at": finish_break_at
        }

    def start_overtime_work_at(self, company_id, employee_id, start_overtime_work_at):
        # 残業開始ボタンを押す
        return {
            "is_working": True,
            "start_overtime_work_at": start_overtime_work_at
        }

    def finish_overtime_work_at(self, company_id, employee_id, finish_overtime_work_at):
        # 残業終了ボタンを押す
        return {
            "is_working": False,
            "finish_overtime_work_at": finish_overtime_work_at
        }

    def work_contents(self, company_id, employee_id, start_work_at, workplace, work_contents):
        # 作業内容を記録する
        return {
            "start_work_at": start_work_at,
            "workplace": workplace,
            "work_contents": work_contents
        }

    def get_monthly_work_records(self, company_id, employee_id, year, month):
        # 月別勤怠情報を取得する
        return {
            "year": year,
            "month": month,
            "work_records": [
                {
                    "start_work_at": "2020-01-01 09:00:00",
                    "finish_work_at": "2020-01-01 18:00:00",
                    "start_break_at": "2020-01-01 12:00:00",
                    "finish_break_at": "2020-01-01 13:00:00",
                    "start_overtime_work_at": "2020-01-01 18:00:00",
                    "finish_overtime_work_at": "2020-01-01 20:00:00",
                    "workplace": "オフィス",
                    "work_contents": "プログラミング"
                },
                {
                    "start_work_at": "2020-01-02 09:00:00",
                    "finish_work_at": "2020-01-02 18:00:00",
                    "start_break_at": "2020-01-02 12:00:00",
                    "finish_break_at": "2020-01-02 13:00:00",
                    "workplace": "オフィス",
                    "work_contents": "プログラミング"
                }
            ]
        }

    def request_correction(self, company_id, employee_id, year, month, correction_date, request_contents):
        # 修正依頼をする
        return {
            "year": year,
            "month": month,
            "correction_date": correction_date,
            "request_contents": request_contents
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
