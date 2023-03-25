import Layout from "@/components/Layout";
import Time from "@/components/Time";

export default function Home() {
  return (
    <Layout>
      <div className="flex flex-col justify-start h-full">
        <div className="text-center">
          <h1 className="text-4xl">
            <Time />
          </h1>
        </div>
      </div>
    </Layout>
  );
}
