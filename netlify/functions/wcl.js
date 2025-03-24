export default async (event, context) => {
  const GUILD_ID = '586445';
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
      console.error('令牌获取失败:', errorText);
      throw new Error(`WCL认证失败: ${tokenRes.status}`);
    }

    const { access_token } = await tokenRes.json();

    // 2. 获取公会数据（设置15秒超时）
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000);

    const apiRes = await fetch(API_URL, {
      headers: { 'Authorization': `Bearer ${access_token}` },
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!apiRes.ok) {
      const apiError = await apiRes.text();
      console.error('API请求失败:', apiError);
      throw new Error(`WCL数据获取失败: ${apiRes.status}`);
    }

    const data = await apiRes.json();

    // 3. 返回数据
    return {
      statusCode: 200,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify(data)
    };

  } catch (error) {
    console.error('完整错误日志:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};