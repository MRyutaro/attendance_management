import axios from "axios";
import { useRouter } from "next/router";
import { useState } from "react";

const Signup = () => {
  const router = useRouter();
  const [email, setemployeeEmail] = useState('');
  const [password, setpassword] = useState('');
  const ApiBaseUrl = "http://localhost:8000/api/";

  const handleSubmit = async (event) => {
    event.preventDefault();

    //フォームの入力値を適切な形式で収集し、APIリクエストに必要なデータを提供
    try {
      const formData = {
        email: email,
        password: password,
      };

      //APIエンドポイントに対してPOSTリクエストを送信
      const response = await axios.post(ApiBaseUrl + "users/signup/", formData);

      // レスポンスのステータスが200の場合は成功
      if (response.status === 200) {
        alert("登録が完了しました");
        // /に遷移
        router.push("/", "/");
      } else {
        alert("登録に失敗しました");
      }

    // エラーハンドリング  
    } catch (error) {
      console.error(error);
      alert("予期しないエラーが発生しました"); 
    }
  };

  //要素の属性や値にアクセス
  const handleChangeEmail = (event) => {
    setemployeeEmail(event.currentTarget.value);
  };

  const handleChangePassword = (event) => {
    setpassword(event.currentTarget.value);
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
                <label htmlFor="email" className="sr-only">
                  メールアドレス
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="メールアドレス"
                  onChange={(event) => handleChangeEmail(event)}
                />
              </div>
              <br></br>
              <div>
                <label htmlFor="password" className="sr-only">
                  パスワード
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="password"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="パスワード"
                  onChange={(event) => handleChangePassword(event)}
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
