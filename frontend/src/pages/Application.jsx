import React from "react";

const Application = () => {
  return (
    <>
      <div>
        <h2>打刻申請状況</h2>
        <div className="bg-gray-100 flex p-4 mt-5 ">
          <section aria-labelledby="open-tickets-tabs-label" className="mr-4 focus:outline-none ">
            <label id="open-tickets-tabs-label" className="font-semibold block mb-1 text-sm">
              申請状況
            </label>
            <ul className="flex">
              <li>
                <button className="focus:outline-none focus:bg-yellow-200 p-2 rounded-l-md border border-r-0 bg-white flex flex-col items-center w-24">
                  <p className="font-semibold text-lg">6</p>
                  <p className="text-sm uppercase text-gray-600">未承認</p>
                </button>
              </li>
              <li>
                <button className="focus:outline-none focus:bg-yellow-200 p-2 rounded-l-md border border-r-0 bg-white flex flex-col items-center w-24">
                  <p className="font-semibold text-lg">6</p>
                  <p className="text-sm uppercase text-gray-600">申請中</p>
                </button>
              </li>
              <li>
                <button className="focus:outline-none focus:bg-yellow-200 p-2 border rounded-r-md bg-white flex flex-col items-center w-24 cursor-pointer">
                  <p className="font-semibold text-lg">23</p>
                  <p className="text-sm uppercase text-gray-600">承認済み</p>
                </button>
              </li>
            </ul>
          </section>
          <div className="flex w-full  gap-y-2">
            <div className="w-full h-[150px] rounded-xl border border-gray-200 bg-white py-4 px-2 shadow-md shadow-gray-100">
              <div className="flex items-center justify-between px-2 text-base font-medium text-gray-700">
                <p>申請エラー</p>
              </div>
              <div className="mt-2">
                <div className="flex max-h-[100px] w-full flex-col overflow-y-scroll">
                  <div className="flex flex-col items-start justify-between font-light text-gray-600">
                    <a className="font-light">2023/04/10 申請が承認されませんでした。再度申請してください</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <h2>打刻申請</h2>
    </>
  );
};

export default Application;
