// 修改后的 wcl-proxy.js
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
    
    // 2. 获取公会报告数据
    const query = `
      query {
        reportData {
          reports(guildID: 586445, limit: 10) {
            data {
              code
              startTime
              title
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
    
    // 3. 验证并格式化数据
    if (!apiData.data?.reportData?.reports?.data) {
      throw new Error('API返回数据格式不正确');
    }

    const reports = apiData.data.reportData.reports.data.map(report => ({
      code: report.code,
      title: report.title || '无标题',
      startTime: report.startTime,
      owner: report.owner ? { name: report.owner.name } : { name: '未知' },
      zone: report.zone ? { name: report.zone.name } : { name: '未知区域' },
      fights: report.fights || []
    }));

    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        data: { reports },
        timestamp: new Date().toISOString()
      })
    };
  } catch (error) {
    console.error('Function执行错误:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      })
    };
  }
};
