import { useEffect, useState } from "react";

const Time = () => {
  const [date, setDate] = useState(new Date());
  const time = date.toLocaleTimeString();
  const day = date.toLocaleDateString();
  useEffect(() => {
    const timerId = setInterval(() => {
      setDate(new Date());
    }, 1000);
    return () => clearInterval(timerId);
  }, [date]);

  return (
    <div className="clock flex">
      <span>{day}</span>
      <br></br>
      <span className="ml-10" suppressHydrationWarning={true}>
        {time}
      </span>
    </div>
  );
};

export default Time;
