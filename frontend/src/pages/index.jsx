import Clock from "../components/Clock";
import Calender from "../components/Clock/Calender";

export default function Home() {
  return (
    <div className="flex flex-col justify-center h-full">
      <div className="text-center">
        <Clock />
        <Calender />
      </div>
    </div>
  );
}
