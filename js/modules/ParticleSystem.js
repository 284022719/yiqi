/**
 * 粒子动画系统
 */
import { CONFIG } from '../config.js';

export class ParticleSystem {
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