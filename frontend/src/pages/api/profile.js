export default function handler(req, res) {
  // GET以外のリクエストを許可しない
  if (req.method.toLocaleLowerCase() !== "get") {
    return res.status(405).end();
  }
  res.status(200).json([{ id: 1, name: "MuneyukiSakata", email: "aaaa.com" }, { id: 2, name: "Ryutaro", email: "bbbbbbb.com" }]);
}
