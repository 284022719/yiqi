require('dotenv').config();
const multipart = require('lambda-multipart-parser'); // 确保这行存在
const cloudinary = require('cloudinary').v2;

cloudinary.config({ 
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME || '默认cloud_name',
  api_key: process.env.CLOUDINARY_API_KEY || '默认api_key',
  api_secret: process.env.CLOUDINARY_API_SECRET || '默认api_secret',
  secure: true // 强制HTTPS
});

exports.handler = async (event) => {
  try {
    console.log('开始处理上传请求');
    
    // 1. 解析表单数据
    const result = await multipart.parse(event);
    if (!result.files || result.files.length === 0) {
      throw new Error('没有接收到文件');
    }
// 在解析表单后添加
if (!result.files || result.files.length === 0) {
  return {
    statusCode: 400,
    body: JSON.stringify({ error: "未接收到文件" })
  };
}

const file = result.files[0];
if (!file.contentType || !file.content) {
  return {
    statusCode: 400,
    body: JSON.stringify({ error: "文件数据不完整" })
  };
}


    const file = result.files[0];
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
    console.log(`接收到文件: ${file.filename}, 类型: ${file.contentType}`);

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

    console.log('上传成功:', uploadResult.secure_url);

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

console.log('当前环境变量:', {
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET ? '已设置' : '未设置'
});