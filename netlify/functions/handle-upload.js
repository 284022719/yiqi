require('dotenv').config();

const crypto = require('crypto');
const multipart = require('lambda-multipart-parser');
const cloudinary = require('cloudinary').v2;

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
  secure: true
});

const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_SIZE = 10 * 1024 * 1024;
const MAX_DESCRIPTION_LENGTH = 200;

/**
 * 可选鉴权：只有部署环境配置了 UPLOAD_TOKEN 时才启用。
 * 未配置时保持旧行为（不阻塞现有上传流程），配置后立即生效。
 */
function readUploadToken(headers) {
  // HTTP/2 与部分网关会改写 header 大小写，这里统一按小写匹配
  for (const [key, value] of Object.entries(headers || {})) {
    if (key.toLowerCase() === 'x-upload-token') {
      return String(value || '');
    }
  }
  return '';
}

function isAuthorized(event) {
  const expected = process.env.UPLOAD_TOKEN;
  if (!expected) return true;

  const provided = readUploadToken(event.headers);
  if (!provided) return false;

  const a = Buffer.from(provided);
  const b = Buffer.from(String(expected));
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(a, b);
}

function sanitizeDescription(raw) {
  if (!raw) return '';
  // Cloudinary context 以 | 分隔键值对，需要剔除分隔符
  return String(raw)
    .replace(/[|\r\n]/g, ' ')
    .trim()
    .slice(0, MAX_DESCRIPTION_LENGTH);
}

function json(statusCode, payload) {
  return {
    statusCode,
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify(payload)
  };
}

exports.handler = async (event) => {
  // 鉴权必须在解析 multipart 之前，否则空 body 会先抛解析异常
  if (!isAuthorized(event)) {
    return json(401, { success: false, error: '未授权：上传口令缺失或不正确' });
  }

  try {
    const result = await multipart.parse(event);

    if (!result.files || result.files.length === 0) {
      return json(400, { success: false, error: '未接收到文件' });
    }

    const file = result.files[0];

    if (!file.contentType || !file.content) {
      return json(400, { success: false, error: '文件数据不完整' });
    }

    if (!ALLOWED_TYPES.includes(file.contentType)) {
      return json(400, { success: false, error: '仅支持 JPEG/PNG/WEBP 格式图片' });
    }

    if (file.content.length > MAX_SIZE) {
      return json(400, { success: false, error: '图片大小不能超过 10MB' });
    }

    const description = sanitizeDescription(result.description);
    const dataURI = `data:${file.contentType};base64,${file.content.toString('base64')}`;

    const uploadResult = await cloudinary.uploader.upload(dataURI, {
      folder: 'guild-uploads',
      resource_type: 'image',
      // 把用户填写的描述持久化，否则刷新后无法还原
      context: description ? `description=${description}` : undefined
    });

    return json(200, {
      success: true,
      url: uploadResult.secure_url,
      public_id: uploadResult.public_id,
      description
    });
  } catch (error) {
    console.error('上传失败:', error.message);

    // 不向客户端回传堆栈与内部细节
    return json(500, { success: false, error: '上传失败，请稍后重试' });
  }
};
