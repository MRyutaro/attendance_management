import axios from "axios";

import Clock from "../components/Clock";
import Calender from "../components/Clock/Calender";

const instance = axios.create({
  baseURL: "http://localhost:8000/api/v1", // APIエンドポイントが存在するサーバーのURL
});
const fetchCompanyData = async () => {
  const response = await instance.get(`/companies/1`);
  const data = response.data;
  console.log(data);
  return data;
};
const CompanyData = async () => {
  const response = await instance.get(`/companies/1`);
  const data = response.data;
  console.log(data);
  return data;
};

export default function Home() {
  return (
    <div className="flex flex-col justify-center h-full">
      <div className="text-center">
        <Clock />
        <Calender />
        <button onClick={CompanyData}>click</button>
      </div>
    </div>
  );
}
