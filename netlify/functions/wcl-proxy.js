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
    
    const tokenData = await tokenResponse.json();
    
    if (!tokenData.access_token) {
      throw new Error('获取访问令牌失败');
    }

    // 2. 使用公会ID查询数据
    const query = `
      query {
        guild(id: 586445) {
          name
          server {
            name
            region {
              id
              name
            }
          }
          attendance(startTime: ${Date.now() - 90 * 24 * 60 * 60 * 1000}) {
            logs {
              startTime
              endTime
              code
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
    
    const data = await apiResponse.json();
    
    return {
      statusCode: 200,
      headers: {
        'Cache-Control': 'public, max-age=3600'
      },
      body: JSON.stringify(data)
    };
  } catch (error) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        error: '获取WCL数据失败',
        details: error.message 
      })
    };
  }
};
