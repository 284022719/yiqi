/**
 * 职业颜色预览组件
 * 用于展示所有魔兽世界职业的官方颜色
 */

import wowClasses from '../data/wow-classes.js';

export default class ClassColorPalette {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) return;
    
    this.render();
  }
  
  render() {
    this.container.innerHTML = '';
    this.container.className = 'color-palette';
    
    wowClasses.forEach(cls => {
      const item = document.createElement('div');
      item.className = 'color-item';
      item.style.cssText = `
        background-color: ${cls.color};
        color: ${cls.textColor};
        border: 1px solid rgba(0,0,0,0.1);
      `;
      
      item.innerHTML = `
        <div class="color-header">
          <strong>${cls.name}</strong>
        </div>
        <div class="color-values">
          <span>${cls.color}</span>
          <button class="copy-btn" data-color="${cls.color}">复制</button>
        </div>
      `;
      
      // 添加复制功能
      const copyBtn = item.querySelector('.copy-btn');
      copyBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        navigator.clipboard.writeText(cls.color);
        copyBtn.textContent = '已复制!';
        setTimeout(() => copyBtn.textContent = '复制', 2000);
      });
      
      this.container.appendChild(item);
    });
  }
} 