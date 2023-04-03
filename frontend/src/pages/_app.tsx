import "../styles/globals.css";

import { AppProps } from "next/app";

import Layout from "../components/Layout";

export default function App(props: AppProps) {
  const { Component, pageProps } = props;
  return (
    <>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </>
  );
}
