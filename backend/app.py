from fastapi import FastAPI
import uvicorn
import json
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"This is": "root"}


@app.get("/api")
def read_api():
    return {"This is": "api"}


@app.get("/api/companies")
def read_companies():
    # dataディレクトリの中のフォルダ名を取得する
    companies = [
        int(d) for d in os.listdir("../data")
        if os.path.isdir(os.path.join("../data", d))
    ]
    return {"companies": companies}


@app.get("/api/companies/{company_id}")
def read_company(company_id: int):
    # data/001/info.jsonからデータを取得する
    with open(f"../data/{company_id}/info.json", "r") as f:
        company_info = json.load(f)
    return {
        "company_id": company_id,
        "company_info": company_info
    }


@app.get("/api/companies/{company_id}/employees")
def read_employees(company_id: int):
    with open(f"../data/{company_id}/info.json", "r") as f:
        employees = json.load(f)["employees"]
    return {
        "company_id": company_id,
        "employees": employees
    }


@app.get("/api/companies/{company_id}/employees/{employee_id}")
def read_employee(company_id: int, employee_id: int):
    with open(f"../data/{company_id}/{employee_id}/info.json", "r") as f:
        employees = json.load(f)
    # ../data/1/1/monthly_data/の中のファイル名の拡張子を除いたものを取得する
    monthly_data = [
        int(d.split(".")[0]) for d in os.listdir(f"../data/{company_id}/{employee_id}/monthly_data")
        if os.path.isfile(os.path.join(f"../data/{company_id}/{employee_id}/monthly_data", d))
    ]

    return {
        "company_id": company_id,
        "employee_id": employee_id,
        "employee_neme": employees["name"],
        "authority": employees["authority"],
        "monthly_data": monthly_data
    }


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
