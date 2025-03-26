// netlify/functions/get-events.js
const { GoogleSpreadsheet } = require('google-spreadsheet');
const moment = require('moment');

exports.handler = async (event, context) => {
  try {
    const { start, end } = event.queryStringParameters;
    
    // 初始化 Google 表格
    const doc = new GoogleSpreadsheet(process.env.GOOGLE_SHEET_ID);
    await doc.useServiceAccountAuth({
      client_email: process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
      private_key: process.env.GOOGLE_PRIVATE_KEY.replace(/\\n/g, '\n')
    });
    
    await doc.loadInfo();
    const sheet = doc.sheetsByIndex[0];
    const rows = await sheet.getRows();
    
    // 过滤和格式化事件
    const events = rows
      .filter(row => {
        const eventDate = moment(row['日期'], 'YYYY-MM-DD');
        return eventDate.isBetween(start, end, null, '[]');
      })
      .map(row => ({
        id: row['ID'],
        title: row['活动名称'],
        start: moment(row['日期'] + ' ' + (row['开始时间'] || '20:00'), 'YYYY-MM-DD HH:mm').toISOString(),
        end: moment(row['日期'] + ' ' + (row['结束时间'] || '23:00'), 'YYYY-MM-DD HH:mm').toISOString(),
        extendedProps: {
          description: row['描述'],
          leader: row['负责人'],
          icon: getActivityIcon(row['活动类型']),
          maxParticipants: row['最大人数'] || ''
        }
      }));
    
    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        events
      })
    };
  } catch (error) {
    console.error('Error fetching events:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
};

function getActivityIcon(activityType) {
  const icons = {
    '团本': 'users',
    '大秘境': 'dungeon',
    'PVP': 'shield-alt',
    '社交': 'glass-cheers'
  };
  return icons[activityType] || 'calendar-alt';
}
