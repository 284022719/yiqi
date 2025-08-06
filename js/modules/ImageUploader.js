/**
 * 图片上传功能
 */
export class ImageUploader {
  constructor() {
    this.uploadForm = document.getElementById('upload-form');
    this.imageUpload = document.getElementById('image-upload');
    this.imagePreview = document.getElementById('image-preview');
    this.imageDescription = document.getElementById('image-description');
    this.uploadStatus = document.getElementById('upload-status');
    this.gallery = document.getElementById('gallery');
  
    if (this.uploadForm) {
      this.init();
    }
  }
  
  init() {
    this.setupEventListeners();
    this.loadGallery();
  }
  
  setupEventListeners() {
    this.imageUpload.addEventListener('change', (e) => this.handleFileSelect(e));
    this.uploadForm.addEventListener('submit', (e) => this.handleFormSubmit(e));
  }
  
  handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    if (!file.type.match('image.*')) {
      this.showStatus('请选择有效的图片文件', 'error');
      return;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
      this.imagePreview.src = e.target.result;
      this.imagePreview.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
  
  async handleFormSubmit(event) {
    event.preventDefault();
    
    try {
      const formData = new FormData(event.target);
      const response = await fetch('/.netlify/functions/handle-upload', {
        method: 'POST',
        body: formData
      });
  
      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.error || '上传失败');
      }
  
      // 获取用户输入的描述
      const description = this.imageDescription.value;
      
      // 添加到画廊
      this.addImageToGallery({
        url: result.url,
        description: description
      });
      
      // 显示成功消息
      this.showStatus('图片上传成功！', 'success');
      
      // 重置表单
      this.resetForm();
      
    } catch (error) {
      this.showStatus(`上传失败: ${error.message}`, 'error');
    }
  }
  
  // 新增方法：直接将图片添加到画廊
  addImageToGallery(image) {
    const galleryItem = document.createElement('div');
    galleryItem.className = 'gallery-item';
    galleryItem.innerHTML = `
      <img src="${image.url}" alt="${image.description}" class="gallery-image zoomable">
      <div class="gallery-caption">${image.description}</div>
    `;
    
    // 添加到画廊开头
    this.gallery.prepend(galleryItem);
    
    // 注册新图片到模态框系统
    if (window.imageModal) {
      window.imageModal.registerImages(galleryItem.querySelectorAll('.gallery-image.zoomable'));
    }
  }
  
  async loadGallery() {
    try {
      const response = await fetch('/.netlify/functions/get-images');
      const images = await response.json();
      
      if (response.ok) {
        this.renderGallery(images);
      } else {
        throw new Error('无法加载图片库');
      }
    } catch (error) {
      console.error('加载图片库错误:', error);
      this.gallery.innerHTML = '<p>暂无上传的图片</p>';
    }
  }
  
  renderGallery(images) {
    if (!images || images.length === 0) {
      this.gallery.innerHTML = '<p>暂无上传的图片</p>';
      return;
    }
    
    this.gallery.innerHTML = images.map(image => `
      <div class="gallery-item">
        <img src="${image.url}" alt="${image.description}" class="gallery-image zoomable">
        <div class="gallery-caption">${image.description}</div>
      </div>
    `).join('');
    
    if (window.imageModal) {
      window.imageModal.registerImages(document.querySelectorAll('.gallery-image.zoomable'));
    }
  }
  
  showStatus(message, type) {
    this.uploadStatus.textContent = message;
    this.uploadStatus.className = 'upload-status';
    this.uploadStatus.classList.add(type);
    
    // 3秒后自动消失
    if (type === 'success') {
      setTimeout(() => {
        this.uploadStatus.textContent = '';
        this.uploadStatus.className = 'upload-status';
      }, 3000);
    }
  }
  
  resetForm() {
    this.uploadForm.reset();
    this.imagePreview.style.display = 'none';
    this.imagePreview.src = '';
  }
} 