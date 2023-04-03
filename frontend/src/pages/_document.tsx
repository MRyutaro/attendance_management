import { createGetInitialProps } from "@mantine/next";
import Document, { Head, Html, Main, NextScript } from "next/document";

import { siteMeta } from "../lib/constants";

const getInitialProps = createGetInitialProps();

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

export default class _Document extends Document {
  static getInitialProps = getInitialProps;

  render() {
    return (
      <Html>
        <Head>
          <Meta siteMeta={siteMeta} />
          <meta name="viewport" content="minimum-scale=1, initial-scale=1, width=device-width" />
          <link rel="icon" href={siteIcon} />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
