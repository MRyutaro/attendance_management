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
      <div className="flex justify-around items-center ">
        <div className="flex justify-around flex-col items-center">
          <div className="flex items-center  text-xl">
            <p className="digit">{date}</p>
            <p className="ml-2">({weekday})</p>
          </div>

          <p className="text-6xl font-bold">{time}</p>
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
    </>
  );
};

export default Clock;
