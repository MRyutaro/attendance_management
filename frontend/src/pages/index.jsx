import Time from "../components/Time";

export default function Home() {
  return (
    <div className="flex flex-col justify-center h-full">
      <div className="text-center">
        <h1 className="text-4xl">
          <Time />
        </h1>
      </div>
    </div>
  );
}
