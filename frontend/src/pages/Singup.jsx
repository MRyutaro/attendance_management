import axios from "axios";
import React, { useState } from "react";

// フォームの入力値を管理
const Signup = () => {
  const [formData, setFormData] = useState({
    company_id: "",
    employee_name: "",
    employee_email: "",
    authority: "",
  });
  
  // フォームの入力値が変更されるたびにフォームデータの状態を更新
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // フォームの送信
  const handleSubmit = async (e) => {
    e.preventDefault();

  try {
  // APIリクエストを実行
    const response = await axios.post(`http://localhost:8000/api/v1/companies/{company_id}/employees`, formData);
    console.log(response.data);// レスポンスのデータを表示 
     
  // 成功したら画面遷移
  
  } catch (error) {
    console.error(error); 
    alert("登録に失敗しました");// エラーハンドリング
  }
};

  return (
    <>
      <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">新規登録</h2>
          </div>
          <form className="mt-8 space-y-6" action="#" method="POST">
            <input type="hidden" name="remember" defaultValue="true" />
            <div className="-space-y-px rounded-md shadow-sm">
              <div>
                <label htmlFor="company_id" className="sr-only">
                  会社ID
                </label>
                <input
                  id="company_id"
                  name="company_id"
                  type="number"
                  autoComplete="company_id"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="会社ID"
                  value={formData.company_id}
                  onChange={handleChange}
                />
              </div>
              <br></br>
              <div>
                <label htmlFor="employee_name" className="sr-only">
                  氏名
                </label>
                <input
                  id="employee_name"
                  name="employee_name"
                  type="text"
                  autoComplete="employee_name"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="氏名"
                  value={formData.employee_name}
                  onChange={handleChange}
                />
              </div>
              <br></br>
              <div>
                <label htmlFor="employee_email" className="sr-only">
                  メールアドレス
                </label>
                <input
                  id="employee_email"
                  name="employee_email"
                  type="email"
                  autoComplete="employee_email"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="メールアドレス"
                  value={formData.employee_email}
                  onChange={handleChange}
                />
              </div>
              <br></br>
              <div>
                <label htmlFor="authority" className="sr-only">
                  パスワード
                </label>
                <input
                  id="authority"
                  name="authority"
                  type="password"
                  autoComplete="authority"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="パスワード"
                  value={formData.authority}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div>
              <button
                onClick={handleSubmit}
                type="submit"
                className="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              >
                <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                  <div className="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" aria-hidden="true" />
                </span>
                登録
              </button>
            </div>
            <div className="justify-between">
              <div className="text-sm"></div>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default Signup;
