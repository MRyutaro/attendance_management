import "../styles/globals.css";

import Layout from "../components/Layout";

export default function App(props) {
  const { Component, pageProps } = props;
  return (
    <>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </>
  );
}
