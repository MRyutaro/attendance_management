import { useRouter } from "next/router";
import { useEffect, useState} from "react";


// これはフックの外部で定義されているため、再利用可能です。
const getCookie = (name) => {
  const cookies = document.cookie.split(";")
    .map(cookie => cookie.trim())
    .reduce((acc, cookie) => {
      const [cookieName, cookieValue] = cookie.split("=");
      acc[cookieName] = cookieValue;
      return acc;
    }, {});

  return cookies[name];
};

const useRequireLogin = () => {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const sessionId = getCookie("sessionid");

    if (!sessionId) {
      router.push("/login", "/login", { shallow: false });
    } else {
      setIsLoading(false);
    }
  }, [router]);

  return isLoading;
};

export default useRequireLogin;
