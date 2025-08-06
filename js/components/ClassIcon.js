/**
 * 职业图标组件
 * 用于显示魔兽世界职业图标和颜色
 */

import wowClasses from '../data/wow-classes.js';
import { getTextColor } from '../data/wow-classes.js';

export default class ClassIcon {
  constructor(classInfo, options = {}) {
    // 配置选项
    const defaults = {
      size: 32,
      showBorder: true,
      showTooltip: true,
      useAltIcon: false,
      isInteractive: true,
      showText: false
    };
    this.options = { ...defaults, ...options };
    
    // 获取职业数据
    this.cls = this.getClassData(classInfo);
    if (!this.cls) return;
    
    // 创建容器元素
    this.element = document.createElement('span');
    this.element.className = 'class-icon';
    this.element.dataset.classId = this.cls.id;
    this.element.dataset.className = this.cls.name;
    
    // 设置图标
    const iconUrl = this.options.useAltIcon && this.cls.iconAlt 
      ? this.cls.iconAlt 
      : this.cls.icon;
    
    this.element.style.cssText = `
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: ${this.options.size}px;
      height: ${this.options.size}px;
      background: url(${iconUrl}) center/contain no-repeat;
      position: relative;
      background-color: ${this.cls.color};
      border-radius: 50%;
    `;
    
    // 添加职业颜色边框
    if (this.options.showBorder) {
      const borderWidth = this.options.size > 40 ? 2 : 1;
      this.element.style.border = `${borderWidth}px solid ${this.cls.borderColor || this.cls.color}`;
    }
    
    // 显示职业首字母（可选）
    if (this.options.showText) {
      const text = document.createElement('span');
      text.textContent = this.cls.name.charAt(0);
      text.style.cssText = `
        font-size: ${this.options.size * 0.5}px;
        font-weight: bold;
        color: ${this.cls.textColor};
        text-shadow: 0 1px 2px rgba(0,0,0,0.7);
      `;
      this.element.appendChild(text);
    }
    
    // 添加工具提示
    if (this.options.showTooltip) {
      this.element.title = this.cls.name;
      this.element.setAttribute('aria-label', `${this.cls.name}职业图标`);
    }
    
    // 添加交互效果
    if (this.options.isInteractive) {
      this.element.style.cursor = 'pointer';
      this.element.style.transition = 'transform 0.2s ease, filter 0.2s ease';
      this.element.addEventListener('mouseenter', () => {
        this.element.style.transform = 'scale(1.1)';
        this.element.style.filter = 'brightness(1.2)';
      });
      this.element.addEventListener('mouseleave', () => {
        this.element.style.transform = 'scale(1)';
        this.element.style.filter = 'none';
      });
    }
  }
  
  getClassData(classInfo) {
    if (typeof classInfo === 'number') {
      return wowClasses.find(c => c.id === classInfo);
    } else if (typeof classInfo === 'string') {
      return wowClasses.find(c => c.slug === classInfo || c.name === classInfo);
    }
    return classInfo;
  }
  
  render(container) {
    if (container && this.element) {
      container.appendChild(this.element);
    }
    return this.element;
  }
} 