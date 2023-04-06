import { useRouter } from "next/router";
import React from "react";

const Singup = () => {
  const router = useRouter();
  const clickHandler = () => {
    router.push("/", "home");
  };
  return (
    <>
      {}
      <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">新規登録</h2>
          </div>
          <form className="mt-8 space-y-6" action="#" method="POST">
            <input type="hidden" name="remember" />
            <div className="-space-y-px rounded-md shadow-sm">
              <div>
                <label htmlFor="password1" className="sr-only">
                  newpassword1
                </label>
                <input
                  id="newpassword1"
                  name="newpassword1"
                  type="newpassword1"
                  autoComplete="newpassword1"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="New password"
                />
              </div>
              <br></br>
              <div>
                <label htmlFor="newpassword2" className="sr-only">
                  newPassword2
                </label>
                <input
                  id="newpassword2"
                  name="newpassword2"
                  type="newpassword2"
                  autoComplete="new-password"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="Check password"
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
                Sing up
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

export default Singup;
