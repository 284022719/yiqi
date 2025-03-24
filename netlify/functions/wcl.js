export default async (event, context) => {
  const GUILD_ID = '你的真实公会ID';
  const AUTH_URL = 'https://www.warcraftlogs.com/oauth/token';
  const API_URL = `https://www.warcraftlogs.com/v1/reports/guild/${GUILD_ID}?region=CN`;

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

    if (!tokenRes.ok) {
      const errorText = await tokenRes.text();
      throw new Error(`令牌获取失败: ${errorText}`);
    }

    const { access_token } = await tokenRes.json();

    // 2. 获取公会数据
    const apiRes = await fetch(API_URL, {
      headers: { 'Authorization': `Bearer ${access_token}` }
    });

    if (!apiRes.ok) {
      const apiError = await apiRes.text();
      throw new Error(`API请求失败: ${apiError}`);
    }

    const data = await apiRes.json();

    // 3. 返回标准Response对象
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { 
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      }
    });

  } catch (error) {
    // 返回标准错误Response
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      }
    });
  }
};