// netlify/functions/gear-stats.js
const { GoogleSpreadsheet } = require('google-spreadsheet');

exports.handler = async (event, context) => {
  try {
    const { class: classFilter, role } = event.queryStringParameters;
    
    // 初始化 Google 表格
    const doc = new GoogleSpreadsheet(process.env.GEAR_SHEET_ID);
    await doc.useServiceAccountAuth({
      client_email: process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
      private_key: process.env.GOOGLE_PRIVATE_KEY.replace(/\\n/g, '\n')
    });
    
    await doc.loadInfo();
    const sheet = doc.sheetsByIndex[0];
    const rows = await sheet.getRows();
    
    // 过滤玩家数据
    let players = rows.map(row => ({
      name: row['角色名'],
      class: row['职业'],
      role: row['职责'],
      itemLevel: parseFloat(row['装等']),
      weapon: row['武器'],
      trinkets: [row['饰品1'], row['饰品2']].filter(Boolean),
      tierSet: parseInt(row['套装'] || 0),
      lastUpdated: row['更新时间']
    }));
    
    // 应用过滤器
    if (classFilter !== 'all') {
      players = players.filter(p => p.class.toLowerCase() === classFilter);
    }
    
    if (role !== 'all') {
      players = players.filter(p => p.role.toLowerCase() === role);
    }
    
    // 计算统计数据
    const avgItemLevel = players.reduce((sum, p) => sum + p.itemLevel, 0) / players.length || 0;
    const maxItemLevel = Math.max(...players.map(p => p.itemLevel), 0);
    const maxItemLevelPlayer = players.find(p => p.itemLevel === maxItemLevel)?.name || '无';
    const avgTierSet = players.reduce((sum, p) => sum + p.tierSet, 0) / players.length || 0;
    
    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        players: players.sort((a, b) => b.itemLevel - a.itemLevel),
        avgItemLevel,
        maxItemLevel,
        maxItemLevelPlayer,
        avgTierSet,
        lastUpdated: new Date().toISOString()
      })
    };
  } catch (error) {
    console.error('Error fetching gear stats:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
};
