const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  const clientId = process.env.WCL_CLIENT_ID;
  const clientSecret = process.env.WCL_CLIENT_SECRET;
  
  // 调试日志
  console.log('开始处理WCL数据请求');
  
  try {
    // 1. 获取访问令牌
    console.log('正在获取访问令牌...');
    const tokenResponse = await fetch('https://www.warcraftlogs.com/oauth/token', {
      method: 'POST',
      headers: {
        'Authorization': 'Basic ' + Buffer.from(`${clientId}:${clientSecret}`).toString('base64'),
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: 'grant_type=client_credentials'
    });
    
    if (!tokenResponse.ok) {
      const errorText = await tokenResponse.text();
      throw new Error(`获取令牌失败: ${tokenResponse.status} - ${errorText}`);
    }
    
    const tokenData = await tokenResponse.json();
    console.log('令牌获取成功');
    
    if (!tokenData.access_token) {
      throw new Error('令牌数据无效: 缺少access_token');
    }

    // 2. 查询公会数据
    console.log('正在查询公会数据...');
    const query = `
      query {
        reportData {
          reports(guildID: 586445, limit: 10) {
            data {
              code
              startTime
              endTime
              owner
              zone {
                name
              }
              fights(killType: Encounters) {
                encounterID
                name
                kill
              }
            }
          }
        }
      }
    `;

    const apiResponse = await fetch('https://www.warcraftlogs.com/api/v2/client', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokenData.access_token}`
      },
      body: JSON.stringify({ query })
    });
    
    if (!apiResponse.ok) {
      const errorText = await apiResponse.text();
      throw new Error(`API请求失败: ${apiResponse.status} - ${errorText}`);
    }
    
    const apiData = await apiResponse.json();
    console.log('公会数据查询成功');
    
    // 3. 返回格式化数据
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=3600'
      },
      body: JSON.stringify({
        success: true,
        data: apiData.data,
        timestamp: new Date().toISOString()
      })
    };
  } catch (error) {
    console.error('处理过程中出错:', error);
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        success: false,
        error: '获取WCL数据失败',
        message: error.message,
        timestamp: new Date().toISOString()
      })
    };
  }
};
