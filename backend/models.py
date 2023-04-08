"""
emailもしくは会社idと従業員idで一意に識別できるようにする
パスワードはハッシュ化して保存する
"""
import psycopg2
import time


class Models():
    def __init__(self):
        # postgresqlに接続する
        self.host = "db"
        self.port = 5432
        self.password = "password"
        self.user = "user"
        self.database = "db"
        # fix: 接続できるまで繰り返す
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                password=self.password,
                user=self.user,
                database=self.database
            )
            conn.close()
        except psycopg2.OperationalError:
            # 数秒待って再接続
            sleep_time = 5
            print(f"postgresqlに接続できませんでした。{sleep_time}秒後に再接続します。")
            time.sleep(sleep_time)
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                password=self.password,
                user=self.user,
                database=self.database
            )
            conn.close()
        self.create_tables()

    def create_tables(self):
        # テーブルを作成する
        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            password=self.password,
            user=self.user,
            database=self.database
        )
        with conn:
            with conn.cursor() as cursor:
                # 会社テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS companies (\
                company_id SERIAL PRIMARY KEY, company_name VARCHAR(30),\
                company_email VARCHAR(30), company_login_password VARCHAR(30))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 従業員テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS employees (\
                employee_id SERIAL PRIMARY KEY, company_id INTEGER,\
                FOREIGN KEY (company_id) REFERENCES companies(company_id),\
                employee_name VARCHAR(30), employee_email VARCHAR(30),\
                authority_code INTEGER, employee_login_password VARCHAR(30))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 勤怠記録テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS work_records (\
                work_record_id SERIAL PRIMARY KEY, employee_id INTEGER,\
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id),\
                work_year INTEGER, work_month INTEGER,\
                work_date DATE, day_of_the_week VARCHAR(30), work_status VARCHAR(30),\
                start_work_at TIME, finish_work_at TIME, start_break_at TIME, finish_break_at TIME,\
                start_overwork_at TIME, finish_overwork_at TIME,\
                workplace VARCHAR(30), work_contents VARCHAR(50))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 勤怠修正依頼テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS correction_requests (\
                    correction_id SERIAL PRIMARY KEY, employee_id INTEGER,\
                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),\
                    correction_date TIMESTAMP, correction_contents VARCHAR(50),\
                    request_date TIMESTAMP, status INTEGER,\
                    confirmed_at TIMESTAMP, confirmed_by INTEGER,\
                    FOREIGN KEY (confirmed_by) REFERENCES employees(employee_id),\
                    reject_reason VARCHAR(50))"
                cursor.execute(sql)
            conn.commit()
            with conn.cursor() as cursor:
                # 有休記録テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS paid_leaves_recodes (\
                    paid_leave_id SERIAL PRIMARY KEY, employee_id INTEGER,\
                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),\
                    paid_leave_date TIMESTAMP, paid_leaves_code INTEGER,\
                    request_date TIMESTAMP, status INTEGER,\
                    confirmed_at TIMESTAMP, confirmed_by INTEGER,\
                    FOREIGN KEY (confirmed_by) REFERENCES employees(employee_id),\
                    reject_reason VARCHAR(50))"
                cursor.execute(sql)
            with conn.cursor() as cursor:
                # 有休日数テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS paid_leaves_days (\
                employee_id INTEGER,\
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id),\
                year INTEGER, max_paid_leaves_days INTEGER,\
                used_paid_leaves_days INTEGER, remaining_paid_leaves_days INTEGER)"
                cursor.execute(sql)

    ######################################################################################
    # ここから管理者用
    ######################################################################################
    def add_company(self, company_name, company_email, company_login_password):
        # 会社を追加する
        # add: ハッシュ化したパスワードをデータベースに保存する
        # add: *で隠して、文字数だけ返す
        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            password=self.password,
            user=self.user,
            database=self.database
        )
        with conn:
            with conn.cursor() as cursor:
                # テーブルを作成
                sql = "CREATE TABLE IF NOT EXISTS companies (company_id SERIAL PRIMARY KEY, company_name VARCHAR(30), company_email VARCHAR(30), company_login_password VARCHAR(30))"
                cursor.execute(sql)
            # コミットしてトランザクション実行
            conn.commit()
            with conn.cursor() as cursor:
                # レコードを挿入
                sql = "INSERT INTO companies (company_name, company_email, company_login_password) VALUES (%s, %s, %s)"
                cursor.execute(sql, (company_name, company_email, company_login_password))
            # コミットしてトランザクション実行
            conn.commit()

        return {
            "company_id": 1,
            "company_name": company_name,
            "company_email": company_email,
            "company_login_password": "*******",
        }

    def get_company(self, company_id):
        # 会社情報を取得する
        return {
            "company_id": company_id,
            "company_name": "株式会社○○",
            "company_email": "aaa.com",
            "company_login_password": "*******",
        }

    def update_company(self, company_id, company_name, company_email, old_company_login_password, new_company_login_password):
        # 会社情報を更新する
        # add: ハッシュ化したパスワードをデータベースに保存する
        # add: *で隠して、文字数だけ返す
        # add: 変更したいときは、古いパスワードを入力する
        return {
            "company_id": company_id,
            "company_name": company_name,
            "company_email": company_email,
            "company_login_password": "*******",
        }

    def add_employee(self, company_id, employee_name, authority_code):
        # 社員を追加する
        # add: idは自動で振られる
        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            password=self.password,
            user=self.user,
            database=self.database
        )
        with conn:
            with conn.cursor() as cursor:
                # 社員を追加する
                sql = "INSERT INTO employees (company_id, employee_name, authority_code) VALUES (%s, %s, %s)"
                cursor.execute(sql)
            # コミットしてトランザクション実行
            conn.commit()
        return {
            "employee_id": 1,
            "employee_name": employee_name,
            "employee_email": "aaa.com",
            "tmp_employee_login_password": "aE9kncIYMXls92jNji9n48HB78b3",
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
