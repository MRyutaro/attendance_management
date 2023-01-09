import Layout from "@/components/Layout";
import Time from "@/components/Time";

export default function Home() {
  return (
    <Layout>
      <div className="flex flex-col justify-center h-full">
        <div className="text-center">
          <h1 className="text-4xl">
            <Time />
          </h1>
        </div>
        <div className="flex flex-col md:flex-row justify-center items-center md:items-start md:justify-around  mt-20">
          <button className="w-[200px] h-[200px] md:w-[230px] md:h-[230px] rounded-full border-2 border-black flex justify-center items-center text-3xl">
            出勤
          </button>
          <button className="w-[200px] h-[200px] md:w-[230px] md:h-[230px] rounded-full border-2 border-black flex justify-center items-center text-3xl md:mt-0 mt-10">
            退勤
          </button>
        </div>
      </div>

      <div>
        aaa
      </div>
    </Layout>
  );
}
