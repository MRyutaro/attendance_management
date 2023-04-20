import { useState } from "react";
import { useRouter } from "next/router";
import axios from "axios";

const Profile = () => {
  const router = useRouter();

  const [formData, setFormData] = useState({
    name: "",
    employee_email: "",
    employee_login_password: "",
    confirmPassword: "",
  });

  const { name, employee_email, employee_login_password, confirmPassword } = formData;

  const onChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = async (e) => {
    e.preventDefault();
    if (employee_login_password !== confirmPassword) {
      console.log("パスワードが間違っています");
    } else {
      try {
        const res = await axios.post("/api/register", {
          name,
          employee_email,
          employee_login_password,
        });
        console.log(res.data);
        router.push("/");
      } catch (err) {
        console.error(err);
      }
    }
  };

  const clickHandler = () => {
    router.push("/", "home");
  };
  return (
    <>
      <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">個人設定</h2>
          </div>
          <form onSubmit={onSubmit} className="mt-8 space-y-6" action="#" method="POST">
            <input type="hidden" name="remember" defaultValue="true" />
            <div className="-space-y-px rounded-md shadow-sm">
              <div>
                <label htmlFor="name" className="sr-only">
                  名前
                </label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  autoComplete="name"
                  onChange={onChange}
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="名前"
                />
              </div>
              <br></br>
              <div>
                <label htmlFor="address" className="sr-only">
                  メールアドレス
                </label>
                <input
                  id="employee_email"
                  name="employee_email"
                  type="text"
                  autoComplete="employee_email"
                  onChange={onChange}
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="メールアドレス"
                />
              </div>
              <br></br>
              <div>
                <label htmlFor="password" className="sr-only">
                  パスワード
                </label>
                <input
                  id="employee_login_password"
                  name="employee_login_password"
                  type="text"
                  autoComplete="employee_login_password"
                  onChange={onChange}
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="パスワード"
                />
              </div>
              <br></br>
              <div>
                <label htmlFor="transportation-expense" className="sr-only">
                  交通費
                </label>
                <input
                  id="transportation-expense"
                  name="transportation-expense"
                  type="number"
                  autoComplete="off"
                  onChange={onChange}
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="交通費"
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
                Submit
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

export default Profile;
