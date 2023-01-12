import Image from "next/image";
import Link from "next/link";
import ApplicationIcon from "public/application.svg";
import HomeIcon from "public/home.svg";
import LogoutIcon from "public/logout.svg";
import MonthlyIcon from "public/monthly.svg";
import ProfileIcon from "public/profile.svg";
import SettingIcon from "public/setting.svg";

const Sidebar = () => {
  return (
    <div className=" static flex flex-col top-0 left-0 w-14 hover:w-[240px] md:w-[200px] bg-[radial-gradient(circle_at_bottom_right,#3c9add,#6a007a)]  h-screen text-white transition-all duration-300 border-none z-10 sidebar">
      <div className="overflow-y-auto overflow-x-hidden flex flex-col justify-between flex-grow">
        <ul className="flex flex-col space-y-1">
          <li className="hidden md:block py-10 ">
            <div className="flex  items-center justify-start w-14 md:w-full ">
              <div className="ml-5">
                <Image
                  src="/dummy-avatar.jpg"
                  height={40}
                  width={40}
                  alt="profile"
                  className="rounded-full  relative object-cover"
                />
              </div>
              <div>
                <p className="ml-5 font-medium group-hover:text-indigo-400 leading-6">
                  Muneyuki Sakata
                </p>
              </div>
            </div>
          </li>
          <li className="px-5 hidden md:block">
            <div className="flex flex-row items-center h-8">
              <div className="text-sm font-light tracking-wide text-gray-400 uppercase">
                Main
              </div>
            </div>
          </li>
          <li>
            <Link
              href="/"
              className="relative flex flex-row items-center h-11 focus:outline-none hover:bg-blue-800 dark:hover:bg-gray-600 text-white-600 hover:text-white-800 border-l-4 border-transparent hover:border-blue-500 dark:hover:border-gray-800 pr-6"
            >
              <span className="inline-flex w-5 h-5 justify-center items-center ml-4 ">
                <HomeIcon />
              </span>
              <span className="ml-2 text-sm tracking-wide truncate">HOME</span>
            </Link>
          </li>
          <li>
            <Link
              href="/Monthly"
              className="relative flex flex-row items-center h-11 focus:outline-none hover:bg-blue-800 dark:hover:bg-gray-600 text-white-600 hover:text-white-800 border-l-4 border-transparent hover:border-blue-500 dark:hover:border-gray-800 pr-6"
            >
              <span className="inline-flex justify-center items-center ml-4">
                <MonthlyIcon />
              </span>
              <span className="ml-2 text-sm tracking-wide truncate">
                Monthly
              </span>
            </Link>
          </li>
          <li>
            <Link
              href="/Application"
              className="relative flex flex-row items-center h-11 focus:outline-none hover:bg-blue-800 dark:hover:bg-gray-600 text-white-600 hover:text-white-800 border-l-4 border-transparent hover:border-blue-500 dark:hover:border-gray-800 pr-6"
            >
              <span className="inline-flex justify-center items-center ml-4">
                <ApplicationIcon />
              </span>
              <span className="ml-2 text-sm tracking-wide truncate">
                Application
              </span>
            </Link>
          </li>
          <li className="px-5 hidden md:block">
            <div className="flex flex-row items-center mt-5 h-8">
              <div className="text-sm font-light tracking-wide text-gray-400 uppercase">
                Settings
              </div>
            </div>
          </li>
          <li>
            <Link
              href="/Profile"
              className="relative flex flex-row items-center h-11 focus:outline-none hover:bg-blue-800 dark:hover:bg-gray-600 text-white-600 hover:text-white-800 border-l-4 border-transparent hover:border-blue-500 dark:hover:border-gray-800 pr-6"
            >
              <span className="inline-flex justify-center items-center ml-4">
                <ProfileIcon />
              </span>
              <span className="ml-2 text-sm tracking-wide truncate">
                Profile
              </span>
            </Link>
          </li>
          <li>
            <Link
              href="/Setting"
              className="relative flex flex-row items-center h-11 focus:outline-none hover:bg-blue-800 dark:hover:bg-gray-600 text-white-600 hover:text-white-800 border-l-4 border-transparent hover:border-blue-500 dark:hover:border-gray-800 pr-6"
            >
              <span className="inline-flex justify-center items-center ml-4">
                <SettingIcon />
              </span>
              <span className="ml-2 text-sm tracking-wide truncate">
                Settings
              </span>
            </Link>
          </li>
        </ul>
        <div className="mb-14 px-5 py-3 hidden md:block text-center focus:outline-none hover:bg-blue-800 dark:hover:bg-gray-600 hover:text-white-800 border-l-4 border-transparent hover:border-blue-500 dark:hover:border-gray-800">
          <Link
            href="/login"
            className="flex items-center mr-4 hover:text-blue-100"
          >
            <span className="inline-flex mr-1">
              <LogoutIcon />
            </span>
            Logout
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
