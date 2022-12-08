import React from "react";

import Footer from "./Footer";
import Meta from "./Meta";
import Sidebar from "./Sidebar";

const Layout = ({ children }) => {
  return (
    <>
      <Meta />
      <Sidebar />
      <main>{children}</main>
      <Footer />
    </>
  );
};

export default Layout;
