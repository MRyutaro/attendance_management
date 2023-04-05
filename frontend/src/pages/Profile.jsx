import { useRouter } from "next/router";

function Profile({ query }) {
  const router = useRouter();
  const clickHandler = () => {
    router.push('/','home')
  }
  return (
    <>
      {}
      <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">プロフィール設定画面</h2>
          </div>
          <form className="mt-8 space-y-6" action="#" method="POST">
            <input type="hidden" name="remember" defaultValue="true" />
            <div className="-space-y-px rounded-md shadow-sm">
              <div>
                <label htmlFor="name" className="sr-only">
                name
                </label>
                <input
                  id="name"
                  name="name"
                  type="name"
                  autoComplete="current-name"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="Name"
                />
              </div>
              <br></br>
              <div>
                <label htmlFor="email" className="sr-only">
                address
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="current-email"
                  required
                  className="relative block w-full appearance-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="Email"
                />
              </div>
            </div>

            <div>
              <button onClick={clickHandler}
                type="submit"
                className="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              >
                <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                  <div className="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" aria-hidden="true" />
                </span>
                submit
              </button>
            </div>
            <div className="justify-between">
              <div className="text-sm">
              </div>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}

export default Profile;

// import axios from "axios";

// export default function Profile(props) {
//   return (
//     <>
//       {props.users.map((user) => {
//         return (
//           <p key={user.id}>
//             <a>名前：{user.name}</a>
//             <a>メールアドレス：{user.email}</a>
//             <br></br>
//           </p>
//         );
//       })}
//     </>
//   );
// }

// export async function getServerSideProps(context) {
//   console.log(
//     "1--------------------------------------------------------------------------------------------------------"
//   );
//   try {
//     const host = "127.0.0.1:8000";
//     const protocol = "http";
//     const url = `${protocol}://${host}/api/profile`;
//     const props = await axios.get(url);
//     const user = props.data;
//     console.log(user);
//     return {
//       props: {
//         user,
//       },
//     };
//   } catch (e) {
//     console.log(e);
//     return {
//       props: {
//         users: [],
//       },
//     };
//   }
// }
