import { useRouter } from "next/router";
import { useEffect } from "react";


const useRequireLogin = () => {
  const router = useRouter();

  useEffect(() => {
    const sessionId = getCookie("sessionid");

    if (!sessionId) {
      router.push("/login", "/login", { shallow: false });
    }
  }, [router]);

  // クッキーから指定された名前の値を取得する関数の実装例
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
};

export default useRequireLogin;
