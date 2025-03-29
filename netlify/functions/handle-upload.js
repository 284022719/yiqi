const cloudinary = require('cloudinary').v2;

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

exports.handler = async (event) => {
  try {
    const result = await multipart.parse(event);
    const file = result.files[0];
    const description = result.description || '未命名图片';

    // 上传到 Cloudinary
    const uploadResult = await cloudinary.uploader.upload(file.content, {
      folder: 'guild-images',
    });

    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        url: uploadResult.secure_url,
        description: description,
      }),
    };
  } catch (error) {
    console.error('上传失败:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: '上传失败',
      }),
    };
  }
};