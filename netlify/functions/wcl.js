export default async (event, context) => {
  const GUILD_ID = '586445'; // 你的公会ID
  const AUTH_URL = 'https://www.warcraftlogs.com/oauth/token';
  const API_URL = `https://cn.warcraftlogs.com/v1/reports/guild/${GUILD_ID}`;

  try {
    // 1. 获取访问令牌
    const auth = Buffer.from(`${process.env.WCL_CLIENT_ID}:${process.env.WCL_CLIENT_SECRET}`).toString('base64');
    const tokenRes = await fetch(AUTH_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${auth}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: 'grant_type=client_credentials'
    });
    const { access_token } = await tokenRes.json();

    // 2. 获取公会数据
    const apiRes = await fetch(API_URL, {
      headers: { 'Authorization': `Bearer ${access_token}` }
    });
    const data = await apiRes.json();

    // 3. 返回数据并设置CORS头
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type'
      },
      body: JSON.stringify(data)
    };

  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: '数据获取失败' })
    };
  }
};