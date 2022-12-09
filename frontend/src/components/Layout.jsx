import Main from "@/components/Main";
import Meta from "@/components/Meta";
import Sidebar from "@/components/Sidebar";

const Layout = ({ children }) => {
  return (
    <>
      <Meta pageTitle="Home"></Meta>
      <div className="flex flex-wrap">
        <Sidebar />
        <Main>{children}</Main>
      </div>
    </>
  );
};

export default Layout;
