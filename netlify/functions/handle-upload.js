require('dotenv').config();
const cloudinary = require('cloudinary').v2;

cloudinary.config({ 
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
  secure: true
});

// 安全的multipart解析函数
function parseMultipartData(event) {
  return new Promise((resolve, reject) => {
    try {
      const boundary = event.headers['content-type']?.split('boundary=')[1];
      if (!boundary) {
        reject(new Error('无法解析multipart边界'));
        return;
      }

      const body = event.body;
      if (event.isBase64Encoded) {
        const buffer = Buffer.from(body, 'base64');
        const parts = buffer.toString('binary').split(`--${boundary}`);
        
        for (const part of parts) {
          if (part.includes('Content-Type:')) {
            const lines = part.split('\r\n');
            let contentType = '';
            let content = '';
            let filename = '';
            
            for (let i = 0; i < lines.length; i++) {
              const line = lines[i];
              if (line.startsWith('Content-Type:')) {
                contentType = line.split(': ')[1];
              } else if (line.startsWith('Content-Disposition:')) {
                const filenameMatch = line.match(/filename="([^"]+)"/);
                if (filenameMatch) {
                  filename = filenameMatch[1];
                }
              } else if (line === '' && i < lines.length - 1) {
                // 空行后的内容是文件数据
                content = lines.slice(i + 1).join('\r\n').replace(/\r\n$/, '');
                break;
              }
            }
            
            if (contentType && content) {
              resolve({
                files: [{
                  contentType,
                  filename,
                  content: Buffer.from(content, 'binary')
                }]
              });
              return;
            }
          }
        }
        reject(new Error('未找到有效的文件数据'));
      } else {
        reject(new Error('请求体必须是base64编码'));
      }
    } catch (error) {
      reject(error);
    }
  });
}

exports.handler = async (event) => {
  try {
    // 1. 解析表单数据
    const result = await parseMultipartData(event);
    
    // 检查文件是否存在
    if (!result.files || result.files.length === 0) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: "未接收到文件" })
      };
    }

    const file = result.files[0];
    
    // 检查文件数据是否完整
    if (!file.contentType || !file.content) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: "文件数据不完整" })
      };
    }

    // ======== 安全增强代码 ========
    // 文件类型检查
    const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
    if (!ALLOWED_TYPES.includes(file.contentType)) {
      throw new Error('仅支持 JPEG/PNG/WEBP 格式图片');
    }
    
    // 文件大小检查（10MB限制）
    const MAX_SIZE = 10 * 1024 * 1024;
    if (file.content.length > MAX_SIZE) {
      throw new Error('图片大小不能超过10MB');
    }
    // ======== 安全增强结束 ========
    
    // 2. 转换为Cloudinary需要的格式
    const fileBuffer = file.content;
    const base64Data = fileBuffer.toString('base64');
    const dataURI = `data:${file.contentType};base64,${base64Data}`;

    // 3. 上传到Cloudinary
    const uploadResult = await cloudinary.uploader.upload(dataURI, {
      folder: 'guild-uploads',
      resource_type: 'auto',
      quality_analysis: true
    });

    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        url: uploadResult.secure_url,
        public_id: uploadResult.public_id
      }),
    };
  } catch (error) {
    console.error('上传失败详情:', {
      error: error.message,
      stack: error.stack
    });
    
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: error.message,
        requestId: event.requestContext?.requestId
      }),
    };
  }
};