/**
 * 一起公会网站 - 主JavaScript文件
 * 功能包含：
 * - 图片模态框系统
 * - 首页粒子动画
 * - WCL数据加载
 */
(function() {
    'use strict'; // 使用严格模式避免常见错误
    
    /*************************
     * 全局配置
     *************************/
    const CONFIG = {
      particleCount: 150,
      particleColors: ['#FFD700', '#785A28', '#FFFFFF', '#FFA500'],
      maxConnectionDistance: 100
    };
    
    /*************************
     * 核心功能实现将放在这里
     *************************/
      /*************************
   * 图片模态框系统
   * 功能：
   * - 点击图片放大显示
   * - 键盘导航(← → ESC)
   * - 响应式适应
   *************************/
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
      
      document.body.insertAdjacentHTML('beforeend', modalHTML);
      
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
      this.updateImage();
      this.modal.style.display = "block";
      document.body.style.overflow = "hidden";
    }
    
    closeModal() {
      this.modal.style.display = "none";
      document.body.style.overflow = "";
    }
    
    showPrevImage() {
      this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
      this.updateImage();
    }
    
    showNextImage() {
      this.currentIndex = (this.currentIndex + 1) % this.images.length;
      this.updateImage();
    }
    
    updateImage() {
      this.modalImg.src = this.images[this.currentIndex].src;
      this.modalImg.alt = this.images[this.currentIndex].alt || '';
    }
    
    registerImages(images) {
      this.images = Array.from(images).filter(img => img.tagName === 'IMG');
      
      this.images.forEach((img, index) => {
        img.style.cursor = 'zoom-in';
        img.addEventListener('click', () => this.openModal(index));
      });
    }
  }
    /*************************
   * 粒子动画系统
   * 功能：
   * - 背景金色粒子动画
   * - 粒子间连线效果
   * - 响应窗口大小变化
   *************************/
    class ParticleSystem {
      constructor() {
       // 自动创建canvas元素如果不存在
        if (!document.getElementById('particle-canvas')) {
          const canvas = document.createElement('canvas');
          canvas.id = 'particle-canvas';
          canvas.style.position = 'fixed';
          canvas.style.top = '0';
          canvas.style.left = '0';
          canvas.style.zIndex = '-1';
          document.body.prepend(canvas);
         }

        this.canvas = document.getElementById('particle-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
    
        this.initCanvas();
        this.createParticles();
        this.startAnimation();
      }
      initCanvas() {
        const resize = () => {
          this.canvas.width = window.innerWidth;
          this.canvas.height = window.innerHeight;
        };
          
        resize();
          window.addEventListener('resize', resize);
        }
        
        createParticles() {
          for (let i = 0; i < CONFIG.particleCount; i++) {
            this.particles.push({
              x: Math.random() * this.canvas.width,
              y: Math.random() * this.canvas.height,
              size: Math.random() * 3 + 1,
              color: CONFIG.particleColors[
                Math.floor(Math.random() * CONFIG.particleColors.length)
              ],
              speedX: Math.random() * 2 - 1,
              speedY: Math.random() * 2 - 1,
              opacity: Math.random() * 0.6 + 0.1
            });
          }
        }
        
        startAnimation() {
          const animate = () => {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            
            this.updateParticles();
            this.drawParticles();
            this.drawConnections();
            
            requestAnimationFrame(animate);
          };
          
          animate();
        }
        
        updateParticles() {
          this.particles.forEach(p => {
            p.x += p.speedX;
            p.y += p.speedY;
            
            // 边界检查
            if (p.x > this.canvas.width || p.x < 0) p.speedX *= -1;
            if (p.y > this.canvas.height || p.y < 0) p.speedY *= -1;
            
            // 随机闪烁
            if (Math.random() > 0.98) p.opacity = Math.random() * 0.6 + 0.1;
          });
        }
        
        drawParticles() {
          this.particles.forEach(p => {
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            this.ctx.fillStyle = p.color;
            this.ctx.globalAlpha = p.opacity;
            this.ctx.fill();
          });
        }
        
        drawConnections() {
          this.ctx.strokeStyle = `rgba(255, 215, 0, 0.3)`;
          this.ctx.lineWidth = 0.5;
          
          for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
              const p1 = this.particles[i];
              const p2 = this.particles[j];
              const distance = Math.sqrt(
                Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2)
              );
              
              if (distance < CONFIG.maxConnectionDistance) {
                const opacity = 0.3 * (1 - distance / CONFIG.maxConnectionDistance);
                this.ctx.strokeStyle = `rgba(255, 215, 0, ${opacity})`;
                
                this.ctx.beginPath();
                this.ctx.moveTo(p1.x, p1.y);
                this.ctx.lineTo(p2.x, p2.y);
                this.ctx.stroke();
              }
            }
          }
        }
      }
        /*************************
   * WCL数据处理器
   * 功能：
   * - 从WCL API加载数据
   * - 显示加载状态和错误
   * - 渲染数据表格
   *************************/
  class WCLDataLoader {
    constructor() {
      this.loadingEl = document.getElementById('loading');
      this.errorEl = document.getElementById('error');
      this.tableEl = document.getElementById('wcl-table');
      
      if (this.tableEl) {
        this.init();
      }
    }
    
    async init() {
      try {
        this.showLoading();
        const reports = await this.fetchReports();
        this.renderReports(reports);
      } catch (error) {
        this.showError(error.message);
      } finally {
        this.hideLoading();
      }
    }
    
    async fetchReports() {
      const response = await fetch('/.netlify/functions/wcl-proxy');
      const data = await response.json();
      
      if (!response.ok || !data.success) {
        throw new Error(data.error || '服务器返回错误');
      }
      
      if (!data.data?.reports) {
        throw new Error('API返回数据格式不正确');
      }
      
      return data.data.reports;
    }
    
    renderReports(reports) {
      if (!reports || reports.length === 0) {
        throw new Error('没有找到近期活动记录');
      }
      
      const tbody = this.tableEl.querySelector('tbody');
      tbody.innerHTML = '';
      
      reports.forEach(report => {
        const row = document.createElement('tr');
        const date = new Date(report.startTime);
        const killCount = report.fights.filter(f => f.kill).length;
        const totalEncounters = new Set(report.fights.map(f => f.encounterID)).size;
        
        row.innerHTML = `
          <td>${date.toLocaleDateString('zh-CN')}</td>
          <td>${report.zone?.name || '未知区域'}</td>
          <td>${killCount}/${totalEncounters}</td>
          <td>${report.owner?.name || '未知'}</td>
          <td>
            <a href="https://www.warcraftlogs.com/reports/${report.code}" 
               target="_blank" 
               class="button wcl-button">
              查看详情
            </a>
          </td>
        `;
        
        tbody.appendChild(row);
      });
      
      this.tableEl.style.display = 'table';
    }
    
    showLoading() {
      this.loadingEl.style.display = 'block';
      this.errorEl.style.display = 'none';
      this.tableEl.style.display = 'none';
    }
    
    hideLoading() {
      this.loadingEl.style.display = 'none';
    }
    
    showError(message) {
      this.errorEl.textContent = message;
      this.errorEl.style.display = 'block';
    }
  }
    /*************************
     * 页面初始化
     *************************/
      function init() {
        // 初始化粒子动画 (所有页面)
        new ParticleSystem();
      
  // 初始化图片模态框 (检查是否有zoomable图片)
  const zoomableImages = document.querySelectorAll('.zoomable');
  if (zoomableImages.length > 0) {
    const imageModal = new ImageModal();
    imageModal.registerImages(zoomableImages);
  }
      
        // 初始化WCL数据 (仅WCL页面)
        if (document.getElementById('wcl-table')) {
          new WCLDataLoader();
        }
      }
    // DOM加载完成后初始化
    document.addEventListener('DOMContentLoaded', init);
  })();