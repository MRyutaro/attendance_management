import os



# if development
import json


class Models():
    def __init__(self):
        # データベースの接続情報を取得する
        pass

    ######################################################################################
    # memberができる操作
    ######################################################################################

    def signup(self, company_id, employee_name, authority, employee_login_password, commuting_expenses):
        # 新規登録する
        pass

    def login(self, company_id, employee_name, user_login_password):
        # ログインする
        pass

    def logout(self):
        # ログアウトする
        pass

    def get_my_information(self, company_id, employee_id):
        # 社員情報を取得する
        pass

    def update_my_information(self, company_id, employee_id, employee_name, authority, employee_login_password, commuting_expenses):
        # 社員情報を更新する
        pass

    def delete_employee(self, company_id, employee_id):
        # 社員情報を削除する
        pass

    def start_work_at(self, company_id, employee_id, start_work_at):
        # 労働開始ボタンを押す
        pass

    def finish_work_at(self, company_id, employee_id, finish_work_at):
        # 労働終了ボタンを押す
        pass

    def start_break_at(self, company_id, employee_id, start_break_at):
        # 休憩開始ボタンを押す
        pass

    def finish_break_at(self, company_id, employee_id, finish_break_at):
        # 休憩終了ボタンを押す
        pass

    def start_overtime_work_at(self, company_id, employee_id, start_overtime_work_at):
        # 残業開始ボタンを押す
        pass

    def finish_overtime_work_at(self, company_id, employee_id, finish_overtime_work_at):
        # 残業終了ボタンを押す
        pass

    def work_contents(self, company_id, employee_id, start_work_at, workplace, work_contents):
        # 作業内容を記録する
        pass

    def get_my_monthly_work_records(self, company_id, employee_id, year, month):
        # 月別勤怠情報を取得する
        pass

    def request_correction(self, company_id, employee_id, year, month, request_contents):
        # 修正依頼をする
        pass

    def get_request_correction(self, company_id, employee_id, year, month):
        # 修正依頼を取得する
        pass

    def request_paid_leave(self, company_id, employee_id, start_paid_leave_at, finish_paid_leave_at):
        # 有給休暇申請をする
        pass

    def get_my_paid_leaves_records(self, company_id, employee_id):
        # 有給休暇申請を取得する
        pass

    def get_my_remaining_paid_leaves_days(self, company_id, employee_id):
        # 残り有給休暇日数を取得する
        pass

    ######################################################################################
    # ここから管理者用
    ######################################################################################

    def get_employees(self, company_id):
        # 全社員情報を取得する
        pass

    def download_monthly_work_records(self, company_id, employee_id, year, month):
        # 月別勤怠情報をダウンロードする
        pass

    def get_correction_requests(self, company_id, employee_id, year, month):
        # 修正依頼を取得する
        pass

    def update_work_records(self, company_id, year, month, start_work_at, finish_work_at, start_break_at, finish_break_at, start_overtime_work_at, finish_overtime_work_at, workplace, work_content):
        # 勤怠情報を更新する
        pass

    def approve_correction(self, company_id, employee_id, year, month):
        # 修正依頼を承認する
        pass

    def reject_correction(self, company_id, employee_id, year, month):
        # 修正依頼を却下する
        pass

    def get_paid_leaves_records(self, company_id):
        # 有給休暇申請を取得する
        pass

    def get_remaining_paid_leaves_days(self, company_id):
        # 残り有給休暇日数を取得する
        pass

    def set_remaining_paid_leaves_days(self, company_id, remaining_paid_leaves_days):
        # 残り有給休暇日数を設定する
        pass

    def update_remaining_paid_leaves_days(self, company_id, remaining_paid_leaves_days):
        # 残り有給休暇日数を更新する
        pass

    def approve_paid_leave(self, company_id, paid_leave_record_id)
        # 有給休暇申請を承認する
        pass

    def reject_paid_leave(self, company_id, paid_leave_record_id)
        # 有給休暇申請を却下する
        pass
