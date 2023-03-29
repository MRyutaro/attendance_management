import Sidebar from "../components/Sidebar";
import Container from "./Container";

const Layout = ({ children }) => {
  return (
    <>
      <main>
        <div className="flex flex-wrap">
          <Sidebar />
          <Container>{children}</Container>
        </div>
      </main>
    </>
  );
};

export default Layout;
