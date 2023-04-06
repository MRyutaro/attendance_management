import { useEffect, useState } from "react";

const Clock = () => {
  const [clockIn, setClockIn] = useState({ date: null, time: null });
  const [clockOut, setClockOut] = useState({ date: null, time: null });
  const [inIsClicked, setInIsClicked] = useState(false);
  const [outIsClicked, setOutIsClicked] = useState(false);
  const [isClockInEdited, setIsClockInEdited] = useState(false);
  const [isClockOutEdited, setIsClockOutEdited] = useState(false);
  const [now, setNow] = useState(new Date());

  let date = now.toLocaleDateString("ja-JP");
  let time = now.toLocaleTimeString("ja-JP", {
    hour12: false,
    hour: "2-digit",
    minute: "2-digit",
  });
  let weekday = now.toLocaleDateString("ja-JP", { weekday: "short" });
  useEffect(() => {
    const interval = setInterval(() => {
      setNow(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleInClick = () => {
    setClockIn({ date: date, time: time });
    setInIsClicked(true);
  };

  const handleOutClick = () => {
    setClockOut({ date: date, time: time });
    setOutIsClicked(true);
  };

  const handleClockInEdit = () => {
    if (!isClockInEdited) {
      const editedTime = prompt("修正後の時刻を入力してください。", clockIn.time);
      if (editedTime !== null) {
        setClockIn({ time: editedTime });
        setIsClockInEdited(true);
      }
    }
  };
  const handleClockOutEdit = () => {
    if (!isClockOutEdited) {
      const editedTime = prompt("修正後の時刻を入力してください。", clockOut.time);
      if (editedTime !== null) {
        setClockOut({ time: editedTime });
        setIsClockOutEdited(true);
      }
    }
  };

  return (
    <>
      <div className="flex justify-around  ">
        <div className="flex justify-around flex-col items-center">
          <div className="flex items-center  text-xl">
            <p className="digit">{date}</p>
            <p className="ml-2">({weekday})</p>
          </div>

          <p suppressHydrationWarning className="text-6xl font-bold">
            {time}
          </p>
        </div>
        <div className="flex flex-col">
          <div className="flex flex-row justify-start items-center md:items-start md:justify-around  ">
            <button onClick={handleInClick} disabled={inIsClicked} className="w-[100px] h-[100px] rounded-full border-2 border-black flex justify-center items-center  text-xl">
              出勤
            </button>

            <button onClick={handleOutClick} disabled={outIsClicked} className="w-[100px] h-[100px] rounded-full border-2 border-black flex justify-center items-center text-xl ml-5">
              退勤
            </button>
          </div>

          <div className="flex flex-col mt-5 ml-5 justify-around items-start">
            <p className="text-sm">
              出勤時刻：
              {clockIn.time && (
                <span>
                  {clockIn.date} {clockIn.time}
                  {isClockInEdited && <span>（修正済み）</span>}
                  <button className={isClockInEdited ? "none" : "ml-5"} onClick={handleClockInEdit} disabled={isClockInEdited}>
                    修正
                  </button>
                </span>
              )}
            </p>
            <p className="text-sm">
              退勤時刻：
              {clockOut.time && (
                <span>
                  {clockOut.date} {clockOut.time}
                  {isClockOutEdited && <span>（修正済み）</span>}
                  <button className={isClockOutEdited ? "none" : "ml-5"} onClick={handleClockOutEdit} disabled={isClockOutEdited}>
                    修正
                  </button>
                </span>
              )}
            </p>
          </div>
        </div>
      </div>
      <div className="">
        <div className="bg-gray-100 flex p-4 mt-5">
          <section aria-labelledby="open-tickets-tabs-label" className="mr-4 focus:outline-none">
            <label id="open-tickets-tabs-label" className="font-semibold block mb-1 text-sm text-left">
              打刻状況
            </label>
            <ul className="flex">
              <li>
                <button className="focus:outline-none focus:bg-yellow-200 p-2 rounded-l-md  border-r-0 bg-white flex flex-col items-center w-24">
                  <p className="font-semibold text-lg">6</p>
                  <p className="text-sm uppercase text-gray-600">打刻漏れ</p>
                </button>
              </li>
              <li>
                <button className="focus:outline-none focus:bg-yellow-200 p-2  bg-white flex flex-col items-center w-24 cursor-pointer">
                  <p className="font-semibold text-lg">3</p>
                  <p className="text-sm uppercase text-gray-600">未申請</p>
                </button>
              </li>

              <li>
                <button className="focus:outline-none focus:bg-yellow-200 p-2  rounded-r-md bg-white flex flex-col items-center w-24 cursor-pointer">
                  <p className="font-semibold text-lg">15</p>
                  <p className="text-sm uppercase text-gray-600">打刻済み</p>
                </button>
              </li>
            </ul>
          </section>
          <div className="flex w-full  gap-y-2">
            <div className="w-full h-[150px] rounded-xl border border-gray-200 bg-white py-4 px-2 shadow-md shadow-gray-100">
              <div className="flex items-center justify-between px-2 text-base font-medium text-gray-700">
                <p>打刻エラー</p>
              </div>
              <div className="mt-2">
                <div className="flex max-h-[100px] w-full flex-col overflow-y-scroll">
                  <div className="flex flex-col items-start justify-between font-light text-gray-600">
                    <a className="font-light">2023/04/10 打刻漏れあります。修正してください</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Clock;
