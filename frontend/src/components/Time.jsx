import { useState } from "react";

const Time = () => {
  const [clockInTime, setClockInTime] = useState(null);
  const [clockOutTime, setClockOutTime] = useState(null);
  const [clockInDate, setClockInDate] = useState(null);
  const [clockOutDate, setClockOutDate] = useState(null);

  let now = new Date();
  let month = now?.getMonth() + 1;
  let day = now?.getDate();
  let hour = now?.getHours().toString().padStart(2, "0");
  let minute = now?.getMinutes().toString().padStart(2, "0");
  let dayOfWeek = now?.getDay();

  const week = ["日", "月", "火", "水", "木", "金", "土"];
  let clockDate = month + "月" + day + "日" + "[" + week[dayOfWeek] + "]";
  let clockTime = hour + ":" + minute;

  const handleInClick = () => {
    setClockInTime(clockTime);
    setClockInDate(clockDate);
  };

  const handleOutClick = () => {
    setClockOutTime(clockTime);
    setClockOutDate(clockDate);
  };

  return (
    <div>
      <div className="flex flex-col md:flex-row justify-center items-center md:items-start md:justify-around  mt-20">
        <button
          onClick={handleInClick}
          className="w-[200px] h-[200px] md:w-[230px] md:h-[230px] rounded-full border-2 border-black flex justify-center items-center text-3xl"
        >
          出勤
        </button>
        <p></p>
        <button
          onClick={handleOutClick}
          className="w-[200px] h-[200px] md:w-[230px] md:h-[230px] rounded-full border-2 border-black flex justify-center items-center text-3xl md:mt-0 mt-10"
        >
          退勤
        </button>
      </div>
      {clockInTime && (
        <p>
          出勤時刻：{clockInDate} {clockInTime}
        </p>
      )}
      {clockOutTime && (
        <p>
          退勤時刻：{clockOutDate} {clockOutTime}
        </p>
      )}
    </div>
  );
};

export default Time;
