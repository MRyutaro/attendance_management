import "../styles/globals.css";

import { MantineProvider } from "@mantine/core";
import { AppProps } from "next/app";
import Head from "next/head";

import Layout from "../components/Layout";
import { siteMeta } from "../lib/constants";

const { siteIcon } = siteMeta;
interface SiteMeta {
  siteTitle: string;
  siteIcon: string;
}

interface MetaProps {
  pageTitle?: string;
  siteMeta: SiteMeta;
}

const Meta: React.FC<MetaProps> = ({ pageTitle, siteMeta }) => {
  const { siteTitle } = siteMeta;
  const title = pageTitle ? `${pageTitle} | ${siteTitle}` : siteTitle;
  return <title>{title}</title>;
};

export default function App(props: AppProps) {
  const { Component, pageProps } = props;
  return (
    <>
      <Head>
        <Meta siteMeta={siteMeta} />
        <meta name="viewport" content="minimum-scale=1, initial-scale=1, width=device-width" />
        <link rel="icon" href={siteIcon} />
      </Head>

      <MantineProvider
        withGlobalStyles
        withNormalizeCSS
        theme={{
          /** Put your mantine theme override here */
          colorScheme: "light",
        }}
      >
        <Layout>
          <Component {...pageProps} />
        </Layout>
      </MantineProvider>
    </>
  );
}
