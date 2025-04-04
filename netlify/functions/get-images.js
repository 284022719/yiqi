const cloudinary = require('cloudinary').v2;

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

exports.handler = async () => {
  try {
    const result = await cloudinary.api.resources({
      type: 'upload',
      prefix: 'guild-uploads/'
    });

    const files = result.resources.map(file => ({
      url: file.secure_url,
      description: file.public_id.split('/').pop().split('.')[0].replace(/-/g, ' ')
    }));

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