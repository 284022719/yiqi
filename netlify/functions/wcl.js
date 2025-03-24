export default async (event, context) => {
  const GUILD_ID = '586445';
  const AUTH_URL = 'https://www.warcraftlogs.com/oauth/token';
  const API_URL = `https://www.warcraftlogs.com/v1/reports/guild/${GUILD_ID}?region=CN`;

  try {
    // 1. 获取访问令牌
    console.log('开始获取访问令牌...');
    const auth = Buffer.from(`${process.env.WCL_CLIENT_ID}:${process.env.WCL_CLIENT_SECRET}`).toString('base64');
    const tokenRes = await fetch(AUTH_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${auth}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: 'grant_type=client_credentials'
    });

    console.log('令牌响应状态:', tokenRes.status);
    if (!tokenRes.ok) {
      const errorText = await tokenRes.text();
      console.error('令牌获取失败详情:', errorText);
      throw new Error(`WCL认证失败: ${errorText}`);
    }

    const { access_token } = await tokenRes.json();
    console.log('访问令牌获取成功');

    // 2. 获取公会数据
    console.log('开始请求API数据...');
    const apiRes = await fetch(API_URL, {
      headers: { 'Authorization': `Bearer ${access_token}` }
    });

    console.log('API响应状态:', apiRes.status);
    if (!apiRes.ok) {
      const apiError = await apiRes.text();
      console.error('API错误详情:', apiError);
      throw new Error(`WCL数据请求失败: ${apiError}`);
    }

    const data = await apiRes.json();
    console.log('API数据解析成功:', data.length, '条记录');

    // 3. 返回标准Response对象
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { 
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      }
    });

  } catch (error) {
    console.error('完整错误堆栈:', error.stack); // 输出堆栈信息
    return new Response(JSON.stringify({ 
      error: error.message,
      stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
    }), {
      status: 500,
      headers: { 
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      }
    });
  }
};