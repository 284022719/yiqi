// 全局模态框系统
class ImageModal {
    constructor() {
      this.modal = null;
      this.modalImg = null;
      this.currentIndex = 0;
      this.images = [];
      
      this.initModal();
      this.setupEventListeners();
    }
    
    initModal() {
      // 创建模态框DOM结构
      const modalHTML = `
        <div id="imageModal" class="modal">
          <span class="modal-close">&times;</span>
          <div class="modal-nav">
            <span class="modal-nav-arrow prev">&#10094;</span>
            <span class="modal-nav-arrow next">&#10095;</span>
          </div>
          <img class="modal-content" id="modalImage">
        </div>
      `;
      
      // 插入到body末尾
      document.body.insertAdjacentHTML('beforeend', modalHTML);
      
      // 获取DOM引用
      this.modal = document.getElementById('imageModal');
      this.modalImg = document.getElementById('modalImage');
    }
    
    setupEventListeners() {
      // 关闭按钮
      document.querySelector('.modal-close').addEventListener('click', () => this.closeModal());
      
      // 点击模态框外部关闭
      this.modal.addEventListener('click', (e) => {
        if (e.target === this.modal) {
          this.closeModal();
        }
      });
      
      // 导航箭头
      document.querySelector('.prev').addEventListener('click', (e) => {
        e.stopPropagation();
        this.showPrevImage();
      });
      
      document.querySelector('.next').addEventListener('click', (e) => {
        e.stopPropagation();
        this.showNextImage();
      });
      
      // 键盘事件
      document.addEventListener('keydown', (e) => {
        if (!this.modal || this.modal.style.display !== 'block') return;
        
        switch(e.key) {
          case 'Escape':
            this.closeModal();
            break;
          case 'ArrowLeft':
            this.showPrevImage();
            break;
          case 'ArrowRight':
            this.showNextImage();
            break;
        }
      });
    }
    
    openModal(index = 0) {
      if (this.images.length === 0) return;
      
      this.currentIndex = index;
      this.modalImg.src = this.images[this.currentIndex].src;
      this.modalImg.alt = this.images[this.currentIndex].alt;
      this.modal.style.display = "block";
      document.body.style.overflow = "hidden"; // 防止背景滚动
    }
    
    closeModal() {
      this.modal.style.display = "none";
      document.body.style.overflow = "";
    }
    
    showPrevImage() {
      this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
      this.modalImg.src = this.images[this.currentIndex].src;
      this.modalImg.alt = this.images[this.currentIndex].alt;
    }
    
    showNextImage() {
      this.currentIndex = (this.currentIndex + 1) % this.images.length;
      this.modalImg.src = this.images[this.currentIndex].src;
      this.modalImg.alt = this.images[this.currentIndex].alt;
    }
    
    registerImages(images) {
      this.images = Array.from(images);
      
      this.images.forEach((img, index) => {
        img.addEventListener('click', () => this.openModal(index));
      });
    }
  }
  
  // 初始化模态框系统
  document.addEventListener('DOMContentLoaded', () => {
    window.imageModal = new ImageModal();
    imageModal.registerImages(document.querySelectorAll('.zoomable'));
  });