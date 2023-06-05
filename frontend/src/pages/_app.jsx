import "../styles/globals.css";

import { AuthProvider } from "../components/Author/AuthProvider";
import Layout from "../components/Layout";

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
