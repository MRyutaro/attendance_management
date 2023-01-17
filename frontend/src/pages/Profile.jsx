import axios from "axios"

import Layout from "@/components/Layout";

export default function Profile(props) {
  return (
    <Layout>
      {props.users.map((user) => {
        return (
          <p key={user.id}>
            <a>名前：{user.name}</a>
            <a>メールアドレス：{user.email}</a>
            <br></br>
          </p>
        );
      })}
    </Layout>
  );
}

export async function getServerSideProps(context) {
  console.log("1--------------------------------------------------------------------------------------------------------");
  try {
    const host = "127.0.0.1:8000";
    const protocol = "http";
    const url = `${protocol}://${host}/api/profile`;
    const props = await axios.get(url);
    const user = props.data;
    console.log(user)
    return {
      props: {
        user,
      },
    };
  }
  catch (e) {
    console.log(e);
    return {
      props: {
        users: [],
      },
    };
  }
}
