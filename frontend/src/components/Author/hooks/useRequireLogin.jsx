import { useRouter } from "next/router";
import { useContext, useEffect } from "react";

import { UserContext } from "../../../utils/Context";

const useRequireLogin = () => {
  const router = useRouter();
  const { user } = useContext(UserContext);

  useEffect(() => {
    if (!user) {
      router.push("/login", "/login", { shallow: false });
    }
  }, [user, router]);
};

export default useRequireLogin;
