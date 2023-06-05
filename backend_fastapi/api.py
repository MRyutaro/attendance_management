import datetime
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
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
async def add_company(request: Request):
    payload = await request.json()

    company_name = payload["company_name"]
    company_email = payload["company_email"]
    company_login_password = payload["company_login_password"]

    return models.add_company(company_name, company_email, company_login_password)


@app.get(api_root + "/companies/{company_id}")
def get_company(company_id: int):
    return models.get_company(company_id)


@app.put(api_root + "/companies/{company_id}")
@app.put(api_root + "/companies/{company_id}")
async def update_company(company_id: int, request: Request):
    payload = await request.json()

    company_name = payload["company_name"]
    company_email = payload["company_email"]
    old_company_login_password = payload["old_company_login_password"]
    new_company_login_password = payload["new_company_login_password"]

    return models.update_company(company_id, company_name, company_email, old_company_login_password, new_company_login_password)


# 従業員を追加する
@app.post(api_root + "/companies/{company_id}/employees")
async def add_employee(company_id: int, request: Request):
    payload = await request.json()

    employee_name = payload["employee_name"]
    employee_email = payload["employee_email"]
    authority = payload["authority"]

    return models.add_employee(company_id, employee_name, employee_email, authority)


# 全従業員の情報を取得する
# クエリパラメータでauthorityを指定すると、その権限の従業員のみを取得する
@app.get(api_root + "/companies/{company_id}/employees")
def get_employees(company_id: int, authority: Optional[str] = None):
    # authorityがADMINかUSERではない場合はエラーを返す
    if authority is not None and authority not in ["ADMIN", "USER"]:
        raise HTTPException(status_code=400, detail="authority must be ADMIN or USER")
    return models.get_employees(company_id, authority)


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
async def login(request: Request):
    payload = await request.json()
    company_id = payload["company_id"]
    employee_email = payload["employee_email"]
    employee_login_password = payload["employee_login_password"]

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
async def update_my_information(company_id: str, employee_id: int, request: Request):
    payload = await request.json()

    employee_name = payload["employee_name"]
    employee_email = payload["employee_email"]
    old_employee_login_password = payload["old_employee_login_password"]
    new_employee_login_password = payload["new_employee_login_password"]
    commuting_expenses = payload["commuting_expenses"]

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
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/work_records/{work_record_id}/work_contents")
async def work_contents(company_id: int, employee_id: int, work_record_id: int, request: Request):
    payload = await request.json()

    workplace = payload["workplace"]
    work_content = payload["work_content"]

    return models.work_contents(company_id, employee_id, work_record_id, workplace, work_content)


# 労働時間記録の一覧を取得する
@app.get(api_root + "/companies/{company_id}/employees/{employee_id}/monthly_work_records/{year}/{month}")
def get_my_monthly_work_records(company_id: int, employee_id: int, year: int, month: int):
    return models.get_monthly_work_records(company_id, employee_id, year, month)


# 勤怠の修正を申請する
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/work_records/{work_record_id}/corrections/request")
async def request_correction(company_id: int, employee_id: int, work_record_id: int, request: Request):
    # TODO: "/companies/{company_id}/employees/{employee_id}/work_records/{work_record_id}/corrections"は修正した内容を見れるエンドポイントにする
    payload = await request.json()

    start_work_at = payload["start_work_at"]
    finish_work_at = payload["finish_work_at"]
    start_break_at = payload["start_break_at"]
    finish_break_at = payload["finish_break_at"]
    start_overwork_at = payload["start_overwork_at"]
    finish_overwork_at = payload["finish_overwork_at"]
    workplace = payload["workplace"]
    work_contents = payload["work_contents"]

    return models.request_correction(company_id, employee_id, work_record_id, start_work_at, finish_work_at, start_break_at, finish_break_at, start_overwork_at, finish_overwork_at, workplace, work_contents)


# 有給の依頼を出す
@app.post(api_root + "/companies/{company_id}/employees/{employee_id}/paid_leaves/request")
async def request_paid_leave(company_id: int, employee_id: int, request: Request):
    payload = await request.json()

    paid_leave_date = payload["paid_leave_date"]
    work_type = payload["work_type"]
    paid_leave_reason = payload["paid_leave_reason"]

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
