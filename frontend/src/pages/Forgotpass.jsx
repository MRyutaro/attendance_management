import { useRouter } from "next/router";

const Forgotpass = () => {
  const router = useRouter();
  const clickHandler = () => {
    router.push("/", "home");
  };

  const submitHandler = (e) => {
    e.preventDefault(); //ブラウザのデフォルトの動作を無効化し、用意した処理を実行
  };

  return (
    <>
      <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">パスワード変更画面</h2>
          </div>
          <form className="mt-8 space-y-6" onSubmit={submitHandler}>
            <input type="hidden" name="remember" defaultValue="true" />
            <div className="-space-y-px rounded-md shadow-sm">
              <div>
                <label htmlFor="password1" className="sr-only">
                  password1
                </label>
                <input
                  id="password1"
                  name="password1"
                  type="password"
                  autoComplete="password1"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="新しいパスワード"
                />
              </div>
              <br></br>
              <div>
                <label htmlFor="password2" className="sr-only">
                  Password2
                </label>
                <input
                  id="password2"
                  name="password2"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="パスワード確認"
                />
              </div>
            </div>

            <div>
              <button
                onClick={clickHandler}
                type="submit"
                className="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              >
                <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                  <div className="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" aria-hidden="true" />
                </span>
                Change
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

export default Forgotpass;
