const cloudinary = require('cloudinary').v2;

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

// Cloudinary 默认 max_results = 10，不显式指定会导致画廊只显示前 10 张
const MAX_RESULTS = 500;

exports.handler = async () => {
  try {
    const result = await cloudinary.api.resources({
      type: 'upload',
      resource_type: 'image',
      prefix: 'guild-uploads/',
      max_results: MAX_RESULTS,
      context: true
    });

    const files = result.resources
      .map((file) => ({
        url: file.secure_url,
        // 优先取上传时写入的 context.description，回退到文件名
        description:
          file.context?.custom?.description ||
          file.public_id.split('/').pop().split('.')[0].replace(/-/g, ' '),
        createdAt: file.created_at || null
      }))
      .sort((a, b) => String(b.createdAt || '').localeCompare(String(a.createdAt || '')));

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=60'
      },
      body: JSON.stringify(files)
    };
  } catch (error) {
    console.error('获取图片错误:', error.message);

    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ error: '无法获取图片' })
    };
  }
};
