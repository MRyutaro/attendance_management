import Document, { Head, Html, Main, NextScript } from "next/document";

import { siteMeta } from "../lib/constants";

const { siteTitle, siteIcon } = siteMeta;

const PageTitle = ({ pageTitle }) => {
  const title = pageTitle ? `${pageTitle} | ${siteTitle}` : siteTitle;
  return <title>{title}</title>;
};

export default class MyDocument extends Document {
  render() {
    const { pageTitle } = this.props;
    return (
      <Html>
        <Head>
          <PageTitle pageTitle={pageTitle} />
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
