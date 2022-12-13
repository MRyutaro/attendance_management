import Meta from "@/components/Meta";
import Sidebar from "@/components/Sidebar";
import Main from "./Main";

const Layout = ({ children }) => {
  return (
    <>
      <Meta></Meta>
      <div className="flex flex-wrap">
        <Sidebar />
        <Main>{children}</Main>
      </div>
    </>
  );
};

export default Layout;
