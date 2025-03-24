export default async () => {
  const GUILD_ID = '586445'; // 替换为真实公会ID
  const AUTH_URL = 'https://cn.warcraftlogs.com/oauth/token';
  const API_URL = `https://cn.warcraftlogs.com/v1/reports/guild/${GUILD_ID}`;

  try {
    // 1. 获取访问令牌
    const auth = Buffer.from(`${process.env.WCL_CLIENT_ID}:${process.env.WCL_CLIENT_SECRET}`).toString('base64');
    const tokenRes = await fetch(AUTH_URL, {
      method: 'POST',
      headers: { 'Authorization': `Basic ${auth}`, 'Content-Type': 'application/x-www-form-urlencoded' },
      body: 'grant_type=client_credentials'
    });
    const { access_token } = await tokenRes.json();

    // 2. 获取公会报告数据
    const apiRes = await fetch(`${API_URL}?limit=10`, { 
      headers: { 'Authorization': `Bearer ${access_token}` } 
    });
    const data = await apiRes.json();

    // 3. 返回响应
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' }
    };

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Access-Control-Allow-Origin': '*' }
    };
  }
};