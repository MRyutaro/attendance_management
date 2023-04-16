import datetime

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models import Models

app = FastAPI()
models = Models()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

api_root = "/api/v1"
port = 8000


@app.get("/")
def root():
    return {"This": "is root path"}


@app.get(api_root + "/")
def api():
    return {"This": "is api root path. 詳しくは/docsを参照してください。"}


######################################################################################
# adminだけができる操作
######################################################################################

# 会社を追加する
@app.post(api_root + "/companies")
def add_company(company_name: str, company_email: str, company_login_password: str):
    return models.add_company(company_name, company_email, company_login_password)


@app.get(api_root + "/companies/{company_id}")
def get_company(company_id: int):
    return models.get_company(company_id)


@app.put(api_root + "/companies/{company_id}")
def update_company(company_id: int, company_name: str = "", company_email: str = "", old_company_login_password: str = "", new_company_login_password: str = ""):
    return models.update_company(company_id, company_name, company_email, old_company_login_password, new_company_login_password)


# 従業員を追加する
@app.post(api_root + "/companies/{company_id}/employees")
def add_employee(company_id: int, employee_name: str, employee_email: str, authority: str):
    return models.add_employee(company_id, employee_name, employee_email, authority)


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


# 従業員の勤怠の修正を却下する
@app.post(api_root + "/companies/{company_id}/monthly_work_records/correction_records/{correction_record_id}/reject")
def reject_correction(company_id: int, year: int, month: int, correction_record_id: int, reject_reason: str):
    return models.reject_correction(company_id, correction_record_id, reject_reason)


# 従業員の有給の依頼記録を取得する
@app.get(api_root + "/companies/{company_id}/paid_leaves_records")
def get_paid_leaves_records(company_id: int, year: int, month: int):
    # add: クエリパラメータで従業員のidを指定できるようにする
    # add: クエリパラメータで承認されていないものだけを取得するようにする
    return models.get_paid_leaves_records(company_id, year, month)


# 有給取得可能日数を設定する
@app.post(api_root + "/companies/{company_id}/paid_leaves_days")
def set_remaining_paid_leave_days(company_id: int, employee_id: int, year: int, max_paid_leaves_days: int):
    return models.set_remaining_paid_leave_days(company_id, employee_id, year, max_paid_leaves_days)


# 従業員の有給の依頼を承認する
@app.post(api_root + "/companies/{company_id}/paid_leaves_records/{paid_leave_record_id}/approve")
def approve_paid_leave(company_id: int, paid_leave_record_id: int):
    return models.approve_paid_leave(company_id, paid_leave_record_id)


# 従業員の有給の依頼を却下する
@app.post(api_root + "/companies/{company_id}/paid_leaves_records/{paid_leave_record_id}/reject")
def reject_paid_leave(company_id: int, paid_leave_record_id: int, reject_reason: str):
    return models.reject_paid_leave(company_id, paid_leave_record_id, reject_reason)


######################################################################################
# 全員ができる操作
######################################################################################

# トークンを取得する
@app.post(api_root + "/token")
def get_token(company_id: int, employee_email: str, employee_login_password: str):
    return models.get_token(company_id, employee_email, employee_login_password)


# ログインする
@app.post(api_root + "/login")
def login(company_id: int, employee_email: str, employee_login_password: str):
    data = models.login(company_id, employee_email, employee_login_password)
    # もしdateにerrorというキーがあれば、それはエラーの内容
    if data["error"] == "company_id or mail address is wrong.":
        raise HTTPException(status_code=401, detail=data["会社IDかメールアドレスが間違っている、もしくは登録されていません。"])
    if data["error"] == "password is wrong.":
        raise HTTPException(status_code=401, detail=data["パスワードが間違っています。"])
    return data


# ログアウトする
@app.get(api_root + "/logout")
def logout():
    return models.logout()


# 社員情報を取得する
@app.get(api_root + "/companies/{company_id}/employees/{employee_id}")
def get_my_information(company_id: int, employee_id: int):
    # fix: 社員情報の型で返す
    return models.get_my_information(company_id, employee_id)


# 社員情報を更新する
@app.put(api_root + "/companies/{company_id}/employees/{employee_id}")
def update_my_information(company_id: str, employee_id: int, old_employee_login_password: str, employee_name: str = "", employee_email: str = "", new_employee_login_password: str = "", commuting_expenses: int = 0):
    return models.update_my_information(company_id, employee_id, employee_name, employee_email, old_employee_login_password, new_employee_login_password, commuting_expenses)


# 労働開始ボタンを押す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/start_work")
def start_work_at(company_id: int, employee_id: int):
    return models.start_work_at(company_id, employee_id)


# 労働終了ボタンを押す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/finish_work")
def finish_work_at(company_id: int, employee_id: int):
    return models.finish_work_at(company_id, employee_id)


# 休憩開始ボタンを押す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/start_break")
def start_break_at(company_id: int, employee_id: int):
    return models.start_break_at(company_id, employee_id)


# 休憩終了ボタンを押す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/finish_break")
def finish_break_at(company_id: int, employee_id: int):
    return models.finish_break_at(company_id, employee_id)


# 残業開始ボタンを押す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/start_overtime_work")
def start_overwork_at(company_id: int, employee_id: int):
    return models.start_overwork_at(company_id, employee_id)


# 残業終了ボタンを押す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/finish_overtime_work")
def finish_overwork_at(company_id: int, employee_id: int):
    return models.finish_overwork_at(company_id, employee_id)


# 業務内容を記録する
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/work_contents")
def work_contents(company_id: int, employee_id: int, work_record_id: int, workplace: str, work_content: str):
    # start_work_atは通常勤務でも残業でもいい。
    return models.work_contents(company_id, employee_id, work_record_id, workplace, work_content)


# 労働時間記録の一覧を取得する
@app.get(api_root + "/companies/{company_id}/employees/{employee_id}/monthly_work_records/{year}/{month}")
def get_my_monthly_work_records(company_id: int, employee_id: int, year: int, month: int):
    return models.get_monthly_work_records(company_id, employee_id, year, month)


# 勤怠の修正を申請する
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/monthly_work_records/{year}/{month}/request_correction")
def request_correction(company_id: int, employee_id: int, work_date: str, start_work_at: str = "", finish_work_at: str = "", start_break_at: str = "", finish_break_at: str = "", start_overwork_at: str = "", finish_overwork_at: str = "", workplace: str = "", work_contents: str = ""):
    # add: request_correction_id
    return models.request_correction(company_id, employee_id, work_date, start_work_at, finish_work_at, start_break_at, finish_break_at, start_overwork_at, finish_overwork_at, workplace, work_contents)


# 有給の依頼を出す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/request_paid_leave")
def request_paid_leave(company_id: int, employee_id: int, paid_leave_date: datetime.date, work_type: str, paid_leave_reason: str):
    # add: request_paid_leave_id
    return models.request_paid_leave(company_id, employee_id, paid_leave_date, work_type, paid_leave_reason)


# 月ごとの有給の依頼記録を取得する
@app.get(api_root + "/companies/{company_id}/employees/{employee_id}/paid_leaves_records/{year}/{month}")
def get_my_paid_leaves_records(company_id: int, employee_id: int, year: int, month: int):
    return models.get_my_paid_leaves_records(company_id, employee_id, year, month)


# 有給取得可能日数を取得する
@app.get(api_root + "/companies/{company_id}/employees/{employee_id}/paid_leaves_days/{year}")
def get_my_paid_leave_days(company_id: int, employee_id: int, year: int):
    return models.get_my_paid_leave_days(company_id, employee_id, year)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
