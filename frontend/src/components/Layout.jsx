import React from "react";

import Footer from "./Footer";
import Meta from "./Meta";
import Sidebar from "./Sidebar";

const Layout = ({ children }) => {
  return (
    <>
      <Meta />
      <div className="flex ">
        <Sidebar />
        <main className="w-4/5">{children}</main>
      </div>
      <Footer />
    </>
  );
};

export default Layout;
