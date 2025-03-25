const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  // 从环境变量获取凭证
  const clientId = process.env.WCL_CLIENT_ID;
  const clientSecret = process.env.WCL_CLIENT_SECRET;
  
  // 从查询参数获取公会信息
  const { guildName, serverName, serverRegion } = event.queryStringParameters;
  
  if (!clientId || !clientSecret) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Missing WCL client credentials' })
    };
  }

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
      throw new Error('Failed to obtain access token');
    }
    
    // 2. 获取公会数据
    const query = `
      query {
        guildData {
          guild(name: "${guildName}", 
                serverSlug: "${serverName}", 
                serverRegion: "${serverRegion}") {
            name
            server {
              name
              region {
                slug
              }
            }
            attendance {
              startTime
              zone {
                name
              }
              total
              logs {
                startTime
                endTime
                code
                owner
                fights {
                  encounterID
                  name
                  kill
                  size
                }
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
      body: JSON.stringify(data)
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        error: 'Failed to fetch WCL data',
        details: error.message 
      })
    };
  }
};