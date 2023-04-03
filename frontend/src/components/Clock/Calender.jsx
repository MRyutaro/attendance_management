import React from "react";

const Calender = () => {
  return (
    <>
      <div className="flex items-center justify-between py-2 ">
        <select
          id="countries"
          class="bg-gray-50 border w-80 border-gray-300 text-gray-900 text-sm  focus:ring-blue-500 focus:border-blue-500 block  p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        >
          <option selected>2023/04</option>
          <option>2023/03</option>
          <option>2023/02</option>
        </select>

        <div className="border rounded-lg px-1">
          <button type="button" className="leading-none rounded-lg transition ease-in-out duration-100 inline-flex cursor-pointer hover:bg-gray-200 p-1 items-center">
            <svg className="h-6 w-6 text-gray-500 inline-flex leading-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div className="border-r inline-flex h-6"></div>
          <button type="button" className="leading-none rounded-lg transition ease-in-out duration-100 inline-flex items-center cursor-pointer hover:bg-gray-200 p-1">
            <svg className="h-6 w-6 text-gray-500 inline-flex leading-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <div className="table w-full mt-5">
        <table className="w-full border">
          <thead>
            <tr className="bg-gray-50 border-b">
              <th className="p-2 border-r cursor-pointer text-sm font-thin text-gray-500">
                <div className="flex items-center justify-center">日付</div>
              </th>
              <th className="p-2 border-r cursor-pointer text-sm font-thin text-gray-500">
                <div className="flex items-center justify-center">勤務区分</div>
              </th>
              <th className="p-2 border-r cursor-pointer text-sm font-thin text-gray-500">
                <div className="flex items-center justify-center">出勤</div>
              </th>
              <th className="p-2 border-r cursor-pointer text-sm font-thin text-gray-500">
                <div className="flex items-center justify-center">退勤</div>
              </th>
              <th className="p-2 border-r cursor-pointer text-sm font-thin text-gray-500">
                <div className="flex items-center justify-center">労働時間</div>
              </th>
              <th className="p-2 border-r cursor-pointer text-sm font-thin text-gray-500">
                <div className="flex items-center justify-center">休憩時間</div>
              </th>
              <th className="p-2 border-r cursor-pointer text-sm font-thin text-gray-500">
                <div className="flex items-center justify-center">残業時間</div>
              </th>
              <th className="p-2 border-r cursor-pointer text-sm font-thin text-gray-500">
                <div className="flex items-center justify-center">備考</div>
              </th>
              <th className="p-2 border-r cursor-pointer text-sm font-thin text-gray-500">
                <div className="flex items-center justify-center">承認</div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr className="bg-gray-100 text-center border-b text-sm text-gray-600">
              <td className="p-2 border-r">04/01（土）</td>
              <td className="p-2 border-r">公休</td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
            </tr>
            <tr className="bg-gray-100 text-center border-b text-sm text-gray-600">
              <td className="p-2 border-r">04/02（日）</td>
              <td className="p-2 border-r">公休</td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
            </tr>
            <tr className=" text-center border-b text-sm text-gray-600">
              <td className="p-2 border-r">04/03（月）</td>
              <td className="p-2 border-r">勤務</td>
              <td className="p-2 border-r">09:00</td>
              <td className="p-2 border-r">19:00</td>
              <td className="p-2 border-r">10:00</td>
              <td className="p-2 border-r">01:00</td>
              <td className="p-2 border-r">01:00</td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
            </tr>
            <tr className=" text-center border-b text-sm text-gray-600">
              <td className="p-2 border-r">04/03（月）</td>
              <td className="p-2 border-r">勤務</td>
              <td className="p-2 border-r">09:00</td>
              <td className="p-2 border-r">19:00</td>
              <td className="p-2 border-r">10:00</td>
              <td className="p-2 border-r">01:00</td>
              <td className="p-2 border-r">01:00</td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
            </tr>
            <tr className=" text-center border-b text-sm text-gray-600">
              <td className="p-2 border-r">04/04（火）</td>
              <td className="p-2 border-r">勤務</td>
              <td className="p-2 border-r">09:00</td>
              <td className="p-2 border-r">19:00</td>
              <td className="p-2 border-r">10:00</td>
              <td className="p-2 border-r">01:00</td>
              <td className="p-2 border-r">01:00</td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
            </tr>
            <tr className=" text-center border-b text-sm text-gray-600">
              <td className="p-2 border-r">04/05（水）</td>
              <td className="p-2 border-r">勤務</td>
              <td className="p-2 border-r">09:00</td>
              <td className="p-2 border-r">19:00</td>
              <td className="p-2 border-r">10:00</td>
              <td className="p-2 border-r">01:00</td>
              <td className="p-2 border-r">01:00</td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
            </tr>
            <tr className=" text-center border-b text-sm text-gray-600">
              <td className="p-2 border-r">04/06（木）</td>
              <td className="p-2 border-r">勤務</td>
              <td className="p-2 border-r">09:00</td>
              <td className="p-2 border-r">19:00</td>
              <td className="p-2 border-r">10:00</td>
              <td className="p-2 border-r">01:00</td>
              <td className="p-2 border-r">01:00</td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
            </tr>
            <tr className=" text-center border-b text-sm text-gray-600">
              <td className="p-2 border-r">04/07（金）</td>
              <td className="p-2 border-r">勤務</td>
              <td className="p-2 border-r">09:00</td>
              <td className="p-2 border-r">19:00</td>
              <td className="p-2 border-r">10:00</td>
              <td className="p-2 border-r">01:00</td>
              <td className="p-2 border-r">01:00</td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
            </tr>
            <tr className="bg-gray-100 text-center border-b text-sm text-gray-600">
              <td className="p-2 border-r">04/08（土）</td>
              <td className="p-2 border-r">公休</td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
            </tr>
            <tr className="bg-gray-100 text-center border-b text-sm text-gray-600">
              <td className="p-2 border-r">04/09（日）</td>
              <td className="p-2 border-r">公休</td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
              <td className="p-2 border-r"></td>
            </tr>
          </tbody>
        </table>
      </div>
    </>
  );
};

export default Calender;
