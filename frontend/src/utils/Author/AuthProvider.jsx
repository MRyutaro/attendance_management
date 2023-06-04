import { useState } from "react";

import { UserContext } from "../../utils/Context";

export const AuthProvider = (props) => {
  const [user, setUser] = useState(null);

  const loginUser = (username) => {
    setUser(username);
  };

  const logoutUser = () => {
    setUser(null);
  };

  return <UserContext.Provider value={{ user, loginUser, logoutUser }}>{props.children}</UserContext.Provider>;
};
