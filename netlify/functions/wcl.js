import fetch from 'node-fetch';

export default async (event, context) => {
  const API_KEY = process.env.WCL_API_KEY;
  const GUILD_ID = "586445"; // 替换真实公会ID

  try {
    const query = `
      query {
        guildData {
          reports(guildID: ${GUILD_ID}, limit: 10) {
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

    const response = await fetch('https://www.warcraftlogs.com/api/v2', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify({ query })
    });

    if (!response.ok) {
      throw new Error(`WCL API Error: ${response.statusText}`);
    }

    const { data } = await response.json();
    return {
      statusCode: 200,
      body: JSON.stringify(data.guildData.reports.data)
    };

  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};