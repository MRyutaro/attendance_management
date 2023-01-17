import Layout from "@/components/Layout";

export default function Profile(props) {
  return (
    <Layout>
      {props.users.map((user) => {
        return(
          <p key={user.id}>
            <a>名前：{user.name}</a>
            <a>メールアドレス：{user.email}</a>
            <br></br>
          </p>
        )
      })}
    </Layout>
  );
}

export async function getServerSideProps(context) {
  try {
    const host = context.req.headers.host || "localhost:5000";
    const protocol = /^localhost/.test(host) ? "http" : "https";
    const users = await fetch(`${protocol}://${host}/api/profile`).then((data) =>
      data.json()
    );
    console.log({users})
    return {
      props: {
        users,
      },
    };
  } catch (e) {
    console.log(e);
    return {
      props: {
        users: [],
      },
    };
  }
}
