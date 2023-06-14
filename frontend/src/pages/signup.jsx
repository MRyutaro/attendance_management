import axios from "axios";
import { useRouter } from "next/router";
import { useState } from "react";

const Signup = () => {
  const router = useRouter();
  const [company_id, setCompanyid] = useState('');
  const [employee_name, setemployeeName] = useState('');
  const [employee_email, setemployeeEmail] = useState('');
  const [authority, setAuthority] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    //フォームの入力値を適切な形式で収集し、APIリクエストに必要なデータを提供
    try {
      const formData = {
        company_id: company_id,
        employee_name: employee_name,
        employee_email: employee_email,
        authority: authority,
      };

      //APIエンドポイントに対してPOSTリクエストを送信
      const response = await axios.post("http://localhost:8000/api/v1/companies/1/employees", formData);
      console.log(response.data);

      // 登録に成功したらホーム画面に遷移
      if (response.data) {
        router.push("/");
      } else {
        alert("登録はできましたが画面遷移ができませんでした");
      }

    // エラーハンドリング  
    } catch (error) {
      console.error(error);
      alert("登録に失敗しました"); 
    }
  };

  //要素の属性や値にアクセス
  const handleChangeId = (event) => {
    setCompanyid(event.currentTarget.value);
  };

  const handleChangeName = (event) => {
    setemployeeName(event.currentTarget.value);
  };

  const handleChangeEmail = (event) => {
    setemployeeEmail(event.currentTarget.value);
  };

  const handleChangeAuthority = (event) => {
    setAuthority(event.currentTarget.value);
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
                  type="text"
                  autoComplete="company_id"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="会社ID"
                  onChange={(event) => handleChangeId(event)}
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
                  onChange={(event) => handleChangeName(event)}
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
                  onChange={(event) => handleChangeEmail(event)}
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
                  onChange={(event) => handleChangeAuthority(event)}
                />
              </div>
            </div>

            <div>
              <button
                onClick={handleSubmit}
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
