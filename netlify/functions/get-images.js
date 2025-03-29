const fs = require('fs');
const path = require('path');

// 假设图片存储在 netlify/large-media 目录下
const IMAGE_DIR = path.join(process.cwd(), 'netlify', 'large-media', 'guild-images');

exports.handler = async () => {
  try {
    // 确保目录存在
    if (!fs.existsSync(IMAGE_DIR)) {
      fs.mkdirSync(IMAGE_DIR, { recursive: true });
      return {
        statusCode: 200,
        body: JSON.stringify([])
      };
    }
    
    // 读取目录中的文件
    const files = fs.readdirSync(IMAGE_DIR)
      .filter(file => /\.(jpg|jpeg|png|gif)$/i.test(file))
      .map(file => {
        return {
          url: `/large-media/guild-images/${file}`,
          description: file.split('.')[0].replace(/-/g, ' ')
        };
      });
    
    return {
      statusCode: 200,
      body: JSON.stringify(files)
    };
  } catch (error) {
    console.error('获取图片错误:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        error: '无法获取图片',
        details: error.message
      })
    };
  }
};