const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  const clientId = process.env.WCL_CLIENT_ID;
  const clientSecret = process.env.WCL_CLIENT_SECRET;
  
  try {
    // 1. 获取访问令牌
    const tokenResponse = await fetch('https://www.warcraftlogs.com/oauth/token', {
      method: 'POST',
      headers: {
        'Authorization': 'Basic ' + Buffer.from(`${clientId}:${clientSecret}`).toString('base64'),
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: 'grant_type=client_credentials'
    });
    
    if (!tokenResponse.ok) {
      throw new Error(`获取令牌失败: ${tokenResponse.status}`);
    }
    
    const tokenData = await tokenResponse.json();
    
    if (!tokenData.access_token) {
      throw new Error('令牌数据无效');
    }

    // 2. 使用正确的GraphQL查询
    const query = `
      query {
        reportData {
          reports(guildID: 586445, limit: 10) {
            data {
              code
              startTime
              endTime
              owner {
                name
              }
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
      throw new Error(`API请求失败: ${apiResponse.status}`);
    }
    
    const apiData = await apiResponse.json();
    
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
