import Head from 'next/head'

import { siteMeta } from '../lib/constants'

const { siteTitle , siteIcon } = siteMeta

const Meta = ({pageTitle}) => {
  const title = pageTitle ? `${pageTitle} | ${siteTitle}` : siteTitle
  return (
    <Head>
      <title>{ title }</title>
      <link rel="icon" href={siteIcon} />
    </Head>
  )
}

export default Meta