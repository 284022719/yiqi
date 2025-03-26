// netlify/functions/rankings.js
const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  try {
    const { tier } = event.queryStringParameters;
    const difficulty = tier === 'mythic' ? 4 : 3; // 4=史诗, 3=英雄
    
    // 1. 获取访问令牌
    const tokenResponse = await fetch('https://www.warcraftlogs.com/oauth/token', {
      method: 'POST',
      headers: {
        'Authorization': 'Basic ' + Buffer.from(`${process.env.WCL_CLIENT_ID}:${process.env.WCL_CLIENT_SECRET}`).toString('base64'),
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: 'grant_type=client_credentials'
    });
    
    if (!tokenResponse.ok) {
      throw new Error(`获取令牌失败: ${tokenResponse.status}`);
    }
    
    const tokenData = await tokenResponse.json();
    
    // 2. 获取公会排行榜数据
    const query = `
      query {
        guildData {
          guild(id: 586445) {
            attendance(difficulty: ${difficulty}, zoneId: -1) {
              edges {
                node {
                  encounter {
                    id
                    name
                  }
                  rankPercent
                  startTime
                  zone {
                    id
                    name
                  }
                  players {
                    name
                    class
                  }
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
    
    if (!apiResponse.ok) {
      throw new Error(`API请求失败:
