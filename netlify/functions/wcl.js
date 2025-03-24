// 使用WCL API v2示例（需替换真实API Key）
export default async (event, context) => {
    const API_KEY = process.env.WCL_API_KEY; // 在Netlify后台设置此环境变量
    const GUILD_ID = "586445"; // 替换为真实公会ID
    
    try {
      const response = await fetch(
        `https://www.warcraftlogs.com/api/v2/guild/${GUILD_ID}?api_key=${API_KEY}`
      );
      const data = await response.json();
      return {
        statusCode: 200,
        body: JSON.stringify(data.data.guild.reports)
      };
    } catch (error) {
      return { statusCode: 500, body: JSON.stringify({ error: "API请求失败" }) };
    }
  };