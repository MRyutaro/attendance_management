import { useState } from "react";

const Time = () => {
  const [clockIn, setClockIn] = useState({ date: null, time: null });
  const [clockOut, setClockOut] = useState({ date: null, time: null });
  const [isClockInEdited, setIsClockInEdited] = useState(false);
  const [isClockOutEdited, setIsClockOutEdited] = useState(false);

  let now = new Date();
  let month = now?.getMonth() + 1;
  let day = now?.getDate();
  let hour = now?.getHours().toString().padStart(2, "0");
  let minute = now?.getMinutes().toString().padStart(2, "0");
  let dayOfWeek = now?.getDay();

  const week = ["日", "月", "火", "水", "木", "金", "土"];
  const date = month + "月" + day + "日" + "[" + week[dayOfWeek] + "]";
  const time = hour + ":" + minute;

  const handleInClick = () => {
    setClockIn({ date: date, time: time });
  };

  const handleOutClick = () => {
    setClockOut({ date: date, time: time });
  };

  const handleClockInEdit = () => {
    if (!isClockInEdited) {
      const editedTime = prompt(
        "修正後の時刻を入力してください。",
        clockIn.time
      );
      if (editedTime !== null) {
        setClockIn({ time: editedTime });
        setIsClockInEdited(true);
      }
    }
  };
  const handleClockOutEdit = () => {
    if (!isClockOutEdited) {
      const editedTime = prompt(
        "修正後の時刻を入力してください。",
        clockOut.time
      );
      if (editedTime !== null) {
        setClockOut({ time: editedTime });
        setIsClockOutEdited(true);
      }
    }
  };

  return (
    <>
      <div className="flex">
        <div className="flex flex-row justify-start items-center md:items-start md:justify-around  mt-5">
          <button
            onClick={handleInClick}
            className="w-[100px] h-[100px] rounded-full border-2 border-black flex justify-center items-center  text-xl"
          >
            出勤
          </button>

          <button
            onClick={handleOutClick}
            className="w-[100px] h-[100px] rounded-full border-2 border-black flex justify-center items-center text-xl ml-5"
          >
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
                <button
                  className={isClockInEdited ? "none" : "ml-5"}
                  onClick={handleClockInEdit}
                  disabled={isClockInEdited}
                >
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
                <button
                  className={isClockOutEdited ? "none" : "ml-5"}
                  onClick={handleClockOutEdit}
                  disabled={isClockOutEdited}
                >
                  修正
                </button>
              </span>
            )}
          </p>
        </div>
      </div>
    </>
  );
};

export default Time;
