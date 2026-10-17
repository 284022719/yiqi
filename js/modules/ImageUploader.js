/**
 * 图片上传与画廊管理
 *
 * 鉴权为可选：仅当服务端配置了 UPLOAD_TOKEN 时，上传接口才会返回 401；
 * 此时前端提示用户输入口令并存入 sessionStorage（关闭标签页即失效）。
 */

const UPLOAD_ENDPOINT = '/.netlify/functions/handle-upload';
const GALLERY_ENDPOINT = '/.netlify/functions/get-images';
const TOKEN_STORAGE_KEY = 'uploadToken';

export class ImageUploader {
  constructor() {
    this.uploadForm = document.getElementById('upload-form');
    this.imageUpload = document.getElementById('image-upload');
    this.imagePreview = document.getElementById('image-preview');
    this.previewPlaceholder = document.getElementById('preview-placeholder');
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

  handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.type.match('image.*')) {
      this.showStatus('请选择有效的图片文件', 'error');
      return;
    }

    const reader = new FileReader();
    reader.onload = (loadEvent) => {
      this.imagePreview.src = loadEvent.target.result;
      this.imagePreview.style.display = 'block';
      if (this.previewPlaceholder) {
        this.previewPlaceholder.style.display = 'none';
      }
    };
    reader.readAsDataURL(file);
  }

  getUploadToken() {
    try {
      return sessionStorage.getItem(TOKEN_STORAGE_KEY) || '';
    } catch {
      return '';
    }
  }

  setUploadToken(token) {
    try {
      sessionStorage.setItem(TOKEN_STORAGE_KEY, token);
    } catch {
      /* sessionStorage 不可用时忽略，下次仍会提示 */
    }
  }

  async sendUpload(formData, token) {
    const headers = token ? { 'x-upload-token': token } : {};
    const response = await fetch(UPLOAD_ENDPOINT, {
      method: 'POST',
      body: formData,
      headers
    });
    const data = await response.json().catch(() => ({}));
    return { response, data };
  }

  async handleFormSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const description = (this.imageDescription?.value || '').trim();

    try {
      let { response, data } = await this.sendUpload(formData, this.getUploadToken());

      // 服务端启用了口令：提示输入后重试一次
      if (response.status === 401) {
        const token = window.prompt('上传需要口令，请输入：');
        if (!token) {
          this.showStatus('已取消上传', 'error');
          return;
        }
        this.setUploadToken(token);
        ({ response, data } = await this.sendUpload(formData, token));
      }

      if (!response.ok) {
        throw new Error(data.error || '上传失败');
      }

      this.addImageToGallery({
        url: data.url,
        description: data.description || description
      });

      this.showStatus('图片上传成功！', 'success');
      this.resetForm();
    } catch (error) {
      this.showStatus(`上传失败: ${error.message}`, 'error');
    }
  }

  addImageToGallery(image) {
    const galleryItem = document.createElement('div');
    galleryItem.className = 'gallery-item';
    galleryItem.innerHTML = `
      <img src="${this.escapeAttr(image.url)}" alt="${this.escapeAttr(image.description)}" class="gallery-image zoomable">
      <div class="gallery-caption">${this.escapeHtml(image.description)}</div>
    `;

    this.gallery.prepend(galleryItem);

    if (window.imageModal) {
      window.imageModal.registerImages(galleryItem.querySelectorAll('.gallery-image.zoomable'));
    }
  }

  async loadGallery() {
    try {
      const response = await fetch(GALLERY_ENDPOINT);
      const images = await response.json();

      if (!response.ok) {
        throw new Error(images.error || '无法加载图片库');
      }

      this.renderGallery(images);
    } catch (error) {
      this.gallery.innerHTML = '<p>暂无上传的图片</p>';
      console.warn('加载图片库失败:', error.message);
    }
  }

  renderGallery(images) {
    if (!Array.isArray(images) || images.length === 0) {
      this.gallery.innerHTML = '<p>暂无上传的图片</p>';
      return;
    }

    this.gallery.innerHTML = images.map((image) => `
      <div class="gallery-item">
        <img src="${this.escapeAttr(image.url)}" alt="${this.escapeAttr(image.description)}" class="gallery-image zoomable">
        <div class="gallery-caption">${this.escapeHtml(image.description)}</div>
      </div>
    `).join('');

    if (window.imageModal) {
      window.imageModal.registerImages(this.gallery.querySelectorAll('.gallery-image.zoomable'));
    }
  }

  showStatus(message, type) {
    this.uploadStatus.textContent = message;
    this.uploadStatus.className = 'upload-status';
    this.uploadStatus.classList.add(type);

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
    if (this.previewPlaceholder) {
      this.previewPlaceholder.style.display = '';
    }
  }

  escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, (char) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[char]);
  }

  escapeAttr(value) {
    return this.escapeHtml(value);
  }
}
