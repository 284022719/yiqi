import fetch from "node-fetch";

export default async (event, context) => {
  const API_KEY = process.env.WCL_API_KEY;
  const GUILD_ID = "586445"; // 替换真实公会ID

  // 调试日志
  console.log("API_KEY exists?", !!API_KEY);
  console.log("Requesting WCL API...");

  try {
    // 修复的 GraphQL 查询
    const query = `
      query {
        guild(id: ${GUILD_ID}) {
          recentReports(limit: 5) {
            data {
              startTime
              zone {
                name
              }
              progress
              duration
            }
          }
        }
      }
    `;

    const response = await fetch("https://www.warcraftlogs.com/api/v2", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${API_KEY}`,
      },
      body: JSON.stringify({ query }),
    });

    // 原始响应文本（用于调试）
    const rawData = await response.text();
    console.log("Raw API response:", rawData);

    if (!response.ok) {
      throw new Error(`WCL API 错误: ${response.status} ${rawData.slice(0, 100)}`);
    }

    const { data, errors } = JSON.parse(rawData);
    
    // 处理 GraphQL 错误
    if (errors) {
      throw new Error(`WCL 数据错误: ${errors[0].message}`);
    }

    return {
      statusCode: 200,
      body: JSON.stringify(data.guild.recentReports.data),
    };
  } catch (error) {
    // 记录完整错误信息
    console.error("函数错误详情:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        error: "服务器开小差了，请联系管理员",
        detail: error.message,
      }),
    };
  }
};