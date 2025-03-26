// netlify/functions/signup-event.js
const { GoogleSpreadsheet } = require('google-spreadsheet');

exports.handler = async (event, context) => {
  try {
    const { eventId } = JSON.parse(event.body);
    
    // 获取用户信息（假设通过Netlify Identity）
    const user = context.clientContext?.user;
    if (!user) {
      throw new Error('需要登录才能报名活动');
    }
    
    // 初始化 Google 表格
    const doc = new GoogleSpreadsheet(process.env.GOOGLE_SHEET_ID);
    await doc.useServiceAccountAuth({
      client_email: process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
      private_key: process.env.GOOGLE_PRIVATE_KEY.replace(/\\n/g, '\n')
    });
    
    await doc.loadInfo();
    const eventsSheet = doc.sheetsByIndex[0];
    const signupsSheet = doc.sheetsByIndex[1] || await doc.addSheet({ title: '报名记录' });
    
    // 查找活动
    const eventRows = await eventsSheet.getRows();
    const event = eventRows.find(row => row['ID'] === eventId);
    if (!event) {
      throw new Error('活动不存在');
    }
    
    // 检查是否已报名
    const signupRows = await signupsSheet.getRows();
    const alreadySignedUp = signupRows.some(row => 
      row['活动ID'] === eventId && row['用户ID'] === user.sub
    );
    
    if (alreadySignedUp) {
      return {
        statusCode: 200,
        body: JSON.stringify({
          success: true,
          message: '您已经报名过此活动'
        })
      };
    }
    
    // 添加报名记录
    await signupsSheet.addRow({
      '活动ID': eventId,
      '活动名称': event['活动名称'],
      '用户ID': user.sub,
      '用户名': user.user_metadata?.full_name || user.email,
      '报名时间': new Date().toISOString(),
      '角色': '待确认',
      '备注': ''
    });
    
    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        message: `成功报名活动: ${event['活动名称']}`
      })
    };
  } catch (error) {
    console.error('Error signing up for event:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
};
