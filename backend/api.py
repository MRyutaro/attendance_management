import datetime

import uvicorn
from fastapi import FastAPI
from models import Models

app = FastAPI()
models = Models()

api_root = "/api/v1"
port = 8000


@app.get("/")
def root():
    return {"This": "is root path"}


@app.get(api_root + "/")
def api():
    return {"This": "is api root path. 詳しくは/docsを参照してください。"}


######################################################################################
# adminができる操作
######################################################################################

# 会社を追加する
@app.post(api_root + "/companies")
def add_company(company_name: str, company_email: str, company_login_password: str):
    return models.add_company(company_name, company_email, company_login_password)


@app.get(api_root + "/companies/{company_id}")
def get_company(company_id: int):
    return models.get_company(company_id)


@app.put(api_root + "/companies/{company_id}")
def update_company(company_id: int, company_name: str, company_email: str, old_company_login_password: str, new_company_login_password: str):
    return models.update_company(company_id, company_name, company_email, old_company_login_password, new_company_login_password)


# 従業員を追加する
@app.post(api_root + "/companies/{company_id}/employees")
def add_employee(company_id: int, employee_email: str):
    return models.add_employee(company_id, employee_email)


# 全従業員の情報を取得する
@app.get(api_root + "/companies/{company_id}/employees")
def get_employees(company_id: int):
    return models.get_employees(company_id)


# 従業員を削除する
@app.delete(api_root + "/companies/{company_id}/employees/{employee_id}")
def delete_employee(company_id: int, employee_id: int):
    return models.delete_employee(company_id, employee_id)


# 特定の従業員の勤怠記録をcsvでダウンロードする
@app.get(api_root + "/companies/{company_id}/employees/{employee_id}/monthly_work_records/{year}/{month}/download")
def download_monthly_work_records(company_id: int, employee_id: int, year: int, month: int):
    return models.download_monthly_work_records(company_id, employee_id, year, month)


# 月ごとの従業員の勤怠の修正依頼を取得する
@app.get(api_root + "/companies/{company_id}/monthly_work_records/{year}/{month}/correction_records")
def get_correction_requests(company_id: int, year: int, month: int):
    # add: クエリパラメータで従業員のidを指定できるようにする
    # add: クエリパラメータで承認されていないものだけを取得するようにする
    return models.get_correction_requests(company_id, year, month)


# 従業員の勤怠の修正を承認する
@app.post(api_root + "/companies/{company_id}/monthly_work_records/correction_records/{correction_record_id}/approve")
def approve_correction(company_id: int, correction_id: int):
    return models.approve_correction(company_id, correction_id)


# 従業員の勤怠を修正する
@app.put(api_root + "/companies/{company_id}/monthly_work_records/{year}/{month}/correction_records")
def update_work_records(company_id: int, year: int, month: int, start_work_at: datetime.datetime, finish_work_at: datetime.datetime, start_break_at: datetime.datetime, finish_break_at: datetime.datetime, start_overtime_work_at: datetime.datetime, finish_overtime_work_at: datetime.datetime, workplace: str, work_content: str):
    # fix: 修正するときに、勤務時間とかを指定するようにする
    # fix: 勤怠記録の型でやり取りするようにする
    return models.update_work_records(company_id, year, month, start_work_at, finish_work_at, start_break_at, finish_break_at, start_overtime_work_at, finish_overtime_work_at, workplace, work_content)


# 従業員の勤怠の修正を却下する
@app.post(api_root + "/companies/{company_id}/monthly_work_records/correction_records/{correction_record_id}/reject")
def reject_correction(company_id: int, year: int, month: int, correction_record_id: int, reject_reason: str):
    return models.reject_correction(company_id, year, month, correction_record_id, reject_reason)


# 従業員の有給の依頼記録を取得する
@app.get(api_root + "/companies/{company_id}/paid_leaves_records")
def get_paid_leaves_records(company_id: int, year: int, month: int):
    # add: クエリパラメータで従業員のidを指定できるようにする
    # add: クエリパラメータで承認されていないものだけを取得するようにする
    return models.get_paid_leaves_records(company_id, year, month)


# 有給取得可能日数を取得する
@app.get(api_root + "/companies/{company_id}/paid_leaves_records/remaining_days")
def get_remaining_paid_leaves_days(company_id: int):
    # fix: 有給取得可能日数をどうやって管理するか考える
    return models.get_remaining_paid_leaves_days(company_id)


# 有給取得可能日数を設定する
@app.post(api_root + "/companies/{company_id}/paid_leaves_records/remaining_days")
def set_remaining_paid_leaves_days(company_id: int, remaining_paid_leaves_days: int):
    return models.set_remaining_paid_leaves_days(company_id, remaining_paid_leaves_days)


# 従業員の有給の依頼を承認する
@app.post(api_root + "/companies/{company_id}/paid_leaves_records/{paid_leave_record_id}/approve")
def approve_paid_leave(company_id: int, paid_leave_record_id: int):
    return models.approve_paid_leave(company_id, paid_leave_record_id)


# 従業員の有給の依頼を却下する
@app.post(api_root + "/companies/{company_id}/paid_leaves_records/{paid_leave_record_id}/reject")
def reject_paid_leave(company_id: int, paid_leave_record_id: int, reject_reason: str):
    return models.reject_paid_leave(company_id, paid_leave_record_id, reject_reason)


######################################################################################
# memberができる操作
######################################################################################


# 新規登録する
@app.post(api_root + "/signup")
def signup(company_id: int, employee_id: int, employee_email: str, employee_name: str, employee_login_password: str):
    # fix: 社員情報の型でやり取りする
    return models.signup(company_id, employee_id, employee_email, employee_name, employee_login_password)


# ログインする
@app.post(api_root + "/login")
def login(company_id: int, employee_id: int, employee_email: str, employee_login_password: str):
    return models.login(company_id, employee_id, employee_email, employee_login_password)


# ログアウトする
@app.get(api_root + "/logout")
def logout():
    return models.logout()


# 社員情報を取得する
@app.get(api_root + "/companies/{company_id}/employees/{employee_id}")
def get_my_information(employee_email: str):
    # fix: 社員情報の型で返す
    return models.get_my_information(employee_email)


# 社員情報を更新する
@app.put(api_root + "/companies/{company_id}/employees/{employee_id}")
def update_my_information(employee_name: str, employee_email: str, old_employee_login_password: str, new_employee_login_password: str, commuting_expenses: int):
    return models.update_my_information(employee_name, employee_email, old_employee_login_password, new_employee_login_password, commuting_expenses)


# 労働開始ボタンを押す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/start_work")
def start_work_at(company_id: int, employee_id: int, start_work_at: datetime.datetime):
    print(company_id, employee_id, start_work_at)
    return models.start_work_at(company_id, employee_id, start_work_at)


# 労働終了ボタンを押す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/finish_work")
def finish_work_at(company_id: int, employee_id: int, finish_work_at: datetime.datetime):
    return models.finish_work_at(company_id, employee_id, finish_work_at)


# 休憩開始ボタンを押す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/start_break")
def start_break_at(company_id: int, employee_id: int, start_break_at: datetime.datetime):
    return models.start_break_at(company_id, employee_id, start_break_at)


# 休憩終了ボタンを押す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/finish_break")
def finish_break_at(company_id: int, employee_id: int, finish_break_at: datetime.datetime):
    return models.finish_break_at(company_id, employee_id, finish_break_at)


# 残業開始ボタンを押す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/start_overtime_work")
def start_overtime_work_at(company_id: int, employee_id: int, start_overtime_work_at: datetime.datetime):
    return models.start_overtime_work_at(company_id, employee_id, start_overtime_work_at)


# 残業終了ボタンを押す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/finish_overtime_work")
def finish_overtime_work_at(company_id: int, employee_id: int, finish_overtime_work_at: datetime.datetime):
    return models.finish_overtime_work_at(company_id, employee_id, finish_overtime_work_at)


# 業務内容を記録する
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/work_contents")
def work_contents(company_id: int, employee_id: int, start_work_at: datetime.datetime, workplace: str, work_content: str):
    # start_work_atは通常勤務でも残業でもいい。
    return models.work_contents(company_id, employee_id, start_work_at, workplace, work_content)


# 労働時間記録の一覧を取得する
@app.get(api_root + "/companies/{company_id}/employees/{employee_id}/monthly_work_records/{year}/{month}")
def get_my_monthly_work_records(company_id: int, employee_id: int, year: int, month: int):
    return models.get_monthly_work_records(company_id, employee_id, year, month)


# 勤怠の修正を申請する
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/monthly_work_records/{year}/{month}/request_correction")
def request_correction(company_id: int, employee_id: int, year: int, month: int, correction_date: datetime.datetime, request_contents: str):
    # add: request_correction_id
    return models.request_correction(company_id, employee_id, year, month, correction_date, request_contents)


# 月ごとの勤怠の修正の申請記録を取得する
@app.get(api_root + "/companies/{company_id}/employees/{employee_id}/monthly_work_records/{year}/{month}/reqyest_corrections")
def get_monthly_request_corrections(company_id: int, employee_id: int, year: int, month: int):
    return models.get_monthly_work_records(company_id, employee_id, year, month)


# 有給の依頼を出す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/request_paid_leave")
def request_paid_leave(company_id: int, employee_id: int, start_paid_leave_at: datetime.datetime, finish_paid_leave_at: datetime.datetime):
    # add: request_paid_leave_id
    return models.request_paid_leave(company_id, employee_id, start_paid_leave_at, finish_paid_leave_at)


# 月ごとの有給の依頼記録を取得する
@app.get(api_root + "/companies/{company_id}/employees/{employee_id}/paid_leaves_records")
def get_my_paid_leaves_records(company_id: int, employee_id: int, year: int, month: int):
    # fix: 自分の情報しか見ない
    return models.get_my_paid_leaves_records(company_id, employee_id, year, month)


# 有給取得可能日数を取得する
@app.get(api_root + "/companies/{company_id}/employees/{employee_id}/paid_leaves_records/remaining_days")
# fix: 有給取得可能日数をどうやって管理するか考える
def get_my_remaining_paid_leaves_days(company_id: int, employee_id: int):
    return models.get_my_remaining_paid_leaves_days(company_id, employee_id)


if __name__ == "__main__":
    uvicorn.run(app, port=port)
