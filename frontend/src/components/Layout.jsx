import Main from "@/components/Main";
import Meta from "@/components/Meta";
import Sidebar from "@/components/Sidebar";

const Layout = ({ children }) => {
  return (
    <>
      <Meta></Meta>
      <div className="flex flex-wrap">
        <Sidebar />
        <main>
          <div className="h-full ml-14 md:ml-64 w-3/4 ">{children}</div>
        </main>
      </div>
    </>
  );
};

export default Layout;
