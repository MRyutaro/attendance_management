import axios from "axios";
import Link from "next/link";
import { useRouter } from "next/router";
import { useState } from "react";

const Login = () => {
  const router = useRouter();
  const [employee_email, setUseremail] = useState("");
  const [employee_login_password, setPassword] = useState("");
  const clickHandler = async (event) => {
    const baseUrl = "http://localhost:8000/api/v1";
    event.preventDefault();

    try {
      const response = await axios.post(
        `${baseUrl}/login`,
        {
          company_id: 1,
          employee_email,
          employee_login_password,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = response.data;

      if (data.is_active) {
        router.push("/", "home");
      } else {
        alert("ログインに失敗しました");
      }
    } catch (error) {
      console.error(error);
      alert("ログインに失敗しました");
    }
  };

  return (
    <>
      <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">ログイン</h2>
          </div>
          <form className="mt-8 space-y-6" action="#" method="POST">
            <input type="hidden" name="remember" defaultValue="true" />
            <div className="-space-y-px rounded-md shadow-sm">
              <div>
                <label htmlFor="email" className="sr-only">
                  Email address
                </label>
                <input
                  id="email"
                  name="email"
                  type="text"
                  autoComplete="current-email"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="Email or Username"
                  value={employee_email}
                  onChange={(event) => setUseremail(event.target.value)}
                />
              </div>
              <br></br>
              <div>
                <label htmlFor="password" className="sr-only">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="text"
                  autoComplete="current-password"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="Password"
                  value={employee_login_password}
                  onChange={(event) => setPassword(event.target.value)}
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="text-sm">
                <Link href="/Forgotpass" className="font-medium text-indigo-600 hover:text-indigo-500">
                  Forgot your password?
                </Link>
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
                Login
              </button>
            </div>
            <div className="justify-between">
              <div className="text-sm">
                <p>Do not have an account?</p>
                <a href="Singup" className="flex justify-end font-medium text-indigo-600 hover:text-indigo-500">
                  Sing Up
                </a>
              </div>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default Login;
