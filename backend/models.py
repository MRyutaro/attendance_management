import os



# if development
import json


class Models():
    def __init__(self):
        # データベースの接続情報を取得する
        pass

    def get_companies(self):
        companies = [
            int(d) for d in os.listdir("../data") if os.path.isdir(os.path.join("../data", d))
        ]

        return {"companies": companies}

    def get_company(self, company_id):
        with open(fr"../data/{company_id}/info.json", "r") as f:
            company_info = json.load(f)

        return {
            "company_id": company_id,
            "company_info": company_info
        }

    def get_employees(self, company_id):
        with open(fr"../data/{company_id}/info.json", "r") as f:
            employees = json.load(f)["employees"]

        return {
            "company_id": company_id,
            "employees": employees
        }

    def get_employee(self, company_id, employee_id):
        with open(fr"../data/{company_id}/{employee_id}/info.json", "r") as f:
            employees = json.load(f)
        # ../../data/1/1/monthly_../data/の中のファイル名の拡張子を除いたものを取得する
        monthly_data = [
            int(d.split(".")[0]) for d in os.listdir(f"../data/{company_id}/{employee_id}/monthly_../data")
            if os.path.isfile(os.path.join(f"../data/{company_id}/{employee_id}/monthly_../data", d))
        ]

        return {
            "company_id": company_id,
            "employee_id": employee_id,
            "employee_neme": employees["name"],
            "authority": employees["authority"],
            "monthly_../data": monthly_data
        }

    def update_employee(self, company_id, employee_id, employee_name, authority, employee_login_password):
        with open(fr"../data/{company_id}/{employee_id}/info.json", "w") as f:
            json.dump({
                "name": employee_name,
                "authority": authority,
                "employee_login_password": employee_login_password
            }, f, indent=4, ensure_ascii=False)

        return {
            "company_id": company_id,
            "employee_id": employee_id,
            "employee_neme": employee_name,
            "authority": authority,
            "employee_login_password": employee_login_password
        }
