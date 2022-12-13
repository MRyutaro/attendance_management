import React from "react";

const Main = ({ children }) => {
  return (
    <main>
      <div className="h-full ml-14 md:ml-64 w-3/4 ">{children}</div>
    </main>
  );
};

export default Main;
