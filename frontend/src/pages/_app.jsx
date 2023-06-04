import "../styles/globals.css";

import Layout from "../components/Layout";
import { AuthProvider } from "../utils/Author/AuthProvider";

export default function App(props) {
  const { Component, pageProps } = props;
  return (
    <>
      <AuthProvider>
        <Layout>
          <Component {...pageProps} />
        </Layout>
      </AuthProvider>
    </>
  );
}
