const fs = require('fs');
const path = require('path');
const multipart = require('lambda-multipart-parser');

// 允许的图片类型
const ALLOWED_MIME_TYPES = [
  'image/jpeg',
  'image/png',
  'image/gif',
  'image/webp'
];
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

exports.handler = async (event) => {
  // 只处理POST请求
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({
        success: false,
        error: 'Method Not Allowed',
        allowedMethods: ['POST']
      })
    };
  }

  try {
    // 解析multipart表单数据
    const result = await multipart.parse(event);
    
    // 验证文件是否存在
    if (!result.files || result.files.length === 0) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          success: false,
          error: '没有上传文件'
        })
      };
    }

    const file = result.files[0];
    const description = result.description || '未命名图片';

    // 验证文件类型
    if (!ALLOWED_MIME_TYPES.includes(file.contentType)) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          success: false,
          error: '不支持的文件类型',
          allowedTypes: ALLOWED_MIME_TYPES
        })
      };
    }

    // 验证文件大小
    if (file.content.length > MAX_FILE_SIZE) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          success: false,
          error: '文件太大',
          maxSize: `${MAX_FILE_SIZE / 1024 / 1024}MB`
        })
      };
    }

    // 创建安全文件名
    const safeDescription = description.replace(/[^a-zA-Z0-9\u4e00-\u9fa5\-_]/g, '');
    const fileExt = path.extname(file.filename) || '.jpg';
    const fileName = `${safeDescription}-${Date.now()}${fileExt}`;
    const uploadDir = path.join(process.cwd(), 'netlify', 'large-media', 'guild-images');
    const filePath = path.join(uploadDir, fileName);

    // 确保目录存在
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }

    // 保存文件
    fs.writeFileSync(filePath, file.content);

    // 返回成功响应
    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        fileName: fileName,
        url: `/large-media/guild-images/${fileName}`,
        description: description,
        fileSize: file.content.length,
        mimeType: file.contentType
      })
    };

  } catch (error) {
    console.error('文件上传处理错误:', error);
    
    // 返回错误响应
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: '处理上传失败',
        details: process.env.NODE_ENV === 'development' ? error.message : undefined
      })
    };
  }
};