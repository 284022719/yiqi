/**
 * 公会成员名单页面逻辑 - 表格版本
 */

class GuildMembersPage {
    constructor() {
        this.currentPage = 1;
        this.pageSize = 25;
        this.currentFilters = {
            search: '',
            class: '',
            realm: '',
            faction: ''
        };
        this.sortConfig = {
            field: 'name',
            direction: 'asc'
        };
        this.allMembers = [];
        this.filteredMembers = [];
        
        // 检测是否为本地开发环境
        this.isLocalDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        this.apiBase = this.isLocalDev ? 'http://localhost:3001' : '/.netlify/functions/database-api';
        
        this.init();
    }
    
    async init() {
        await this.loadStatistics();
        await this.loadFilters();
        await this.loadMembers();
        this.setupEventListeners();
    }
    
    async loadStatistics() {
        try {
            const response = await fetch(`${this.apiBase}?action=statistics`);
            const data = await response.json();
            
            if (data.success) {
                this.renderStatistics(data.data);
            } else {
                console.error('加载统计数据失败:', data.error);
                this.showError('加载统计数据失败');
            }
        } catch (error) {
            console.error('加载统计数据时出错:', error);
            this.showError('加载统计数据时出错');
        }
    }
    
    renderStatistics(stats) {
        const container = document.getElementById('stats-summary');
        
        container.innerHTML = `
            <div class="stat-card">
                <div class="stat-number">${stats.total_members || 0}</div>
                <div class="stat-label">总成员数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${Object.keys(stats.server_distribution || {}).length}</div>
                <div class="stat-label">服务器数量</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${stats.active_members || 0}</div>
                <div class="stat-label">活跃成员</div>
            </div>
        `;
    }
    
    async loadFilters() {
        try {
            // 加载职业选项
            const classResponse = await fetch(`${this.apiBase}?action=classes`);
            const classData = await classResponse.json();
            
            if (classData.success) {
                const classSelect = document.getElementById('class-filter');
                classData.data.forEach(className => {
                    const option = document.createElement('option');
                    option.value = className;
                    option.textContent = className;
                    classSelect.appendChild(option);
                });
            }
            
            // 加载服务器选项
            const realmResponse = await fetch(`${this.apiBase}?action=realms`);
            const realmData = await realmResponse.json();
            
            if (realmData.success) {
                const realmSelect = document.getElementById('realm-filter');
                realmData.data.forEach(realmName => {
                    const option = document.createElement('option');
                    option.value = realmName;
                    option.textContent = realmName;
                    realmSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('加载筛选选项时出错:', error);
            this.showError('加载筛选选项时出错');
        }
    }
    
    async loadMembers() {
        try {
            const response = await fetch(`${this.apiBase}?action=members&limit=1000`);
            const data = await response.json();
            
            if (data.success) {
                this.allMembers = data.data.members || [];
                this.applyFilters();
            } else {
                console.error('加载成员数据失败:', data.error);
                this.showError('加载成员数据失败');
            }
        } catch (error) {
            console.error('加载成员数据时出错:', error);
            this.showError('加载成员数据时出错');
        }
    }
    
    applyFilters() {
        this.filteredMembers = this.allMembers.filter(member => {
            const matchesSearch = !this.currentFilters.search || 
                member.name.toLowerCase().includes(this.currentFilters.search.toLowerCase()) ||
                member.realm_name.toLowerCase().includes(this.currentFilters.search.toLowerCase());
            
            const matchesClass = !this.currentFilters.class || 
                member.class === this.currentFilters.class;
            
            const matchesRealm = !this.currentFilters.realm || 
                member.realm_name === this.currentFilters.realm;
            
            const matchesFaction = !this.currentFilters.faction || 
                member.faction === this.currentFilters.faction;
            
            return matchesSearch && matchesClass && matchesRealm && matchesFaction;
        });
        
        this.sortMembers();
        this.currentPage = 1;
        this.renderMembers();
        this.renderPagination();
    }
    
    sortMembers() {
        const { field, direction } = this.sortConfig;
        
        this.filteredMembers.sort((a, b) => {
            let aValue = a[field];
            let bValue = b[field];
            
            // 处理数值类型
            if (typeof aValue === 'number' && typeof bValue === 'number') {
                return direction === 'asc' ? aValue - bValue : bValue - aValue;
            }
            
            // 处理字符串类型
            if (typeof aValue === 'string' && typeof bValue === 'string') {
                aValue = aValue.toLowerCase();
                bValue = bValue.toLowerCase();
                if (direction === 'asc') {
                    return aValue.localeCompare(bValue);
                } else {
                    return bValue.localeCompare(aValue);
                }
            }
            
            // 处理null/undefined值
            if (aValue === null || aValue === undefined) aValue = '';
            if (bValue === null || bValue === undefined) bValue = '';
            
            return direction === 'asc' ? 
                String(aValue).localeCompare(String(bValue)) : 
                String(bValue).localeCompare(String(aValue));
        });
    }
    
    renderMembers() {
        const tbody = document.getElementById('members-tbody');
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const endIndex = startIndex + this.pageSize;
        const pageMembers = this.filteredMembers.slice(startIndex, endIndex);
        
        if (pageMembers.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="9" class="no-results">
                        <i class="fas fa-search"></i>
                        <p>没有找到匹配的成员</p>
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = pageMembers.map(member => this.createMemberRow(member)).join('');
    }
    
    createMemberRow(member) {
        const classColor = this.getClassColor(member.class);
        const lastOnline = this.formatLastOnline(member.last_online_days);
        const mythicScore = member.mythic_score || 0;
        const achievementPoints = member.achievement_points || 0;
        const itemLevel = member.average_item_level || 0;
        const factionColor = member.faction === 'Horde' ? '#C41F3B' : '#0070DE';
        
        return `
            <tr class="member-row">
                <td class="member-name">
                    <img src="./img/class-icons/${this.getClassIconPath(member.class)}" alt="${member.class}" class="class-icon" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">
                    <span style="color: ${classColor}; font-weight: bold;">${member.name}</span>
                </td>
                <td class="member-realm">${member.realm_name}</td>
                <td class="member-class">
                    <span style="color: ${classColor};">${member.class}</span>
                </td>
                <td class="member-level">
                    <span class="level-text">${member.level || 0}</span>
                </td>
                <td class="member-mythic">
                    <span class="score-value">${mythicScore.toLocaleString()}</span>
                </td>
                <td class="member-achievement">
                    <span class="score-value">${achievementPoints.toLocaleString()}</span>
                </td>
                <td class="member-itemlevel">
                    <span class="score-value">${itemLevel.toFixed(1)}</span>
                </td>
                <td class="member-online">
                    <span class="online-status">${lastOnline}</span>
                </td>
                <td class="member-faction">
                    <img src="./img/faction-icons/${this.getFactionIconPath(member.faction)}" alt="${member.faction}" class="faction-icon" style="width: 16px; height: 16px; margin-right: 4px; vertical-align: middle;">
                    <span style="color: ${factionColor}; margin-left: 4px;">${member.faction}</span>
                </td>
            </tr>
        `;
    }
    
    getClassColor(className) {
        const colors = {
            '战士': '#C79C6E',
            '法师': '#69CCF0',
            '猎人': '#ABD473',
            '圣骑士': '#F58CBA',
            '牧师': '#FFFFFF',
            '潜行者': '#FFF569',
            '死亡骑士': '#C41F3B',
            '萨满祭司': '#0070DE',
            '术士': '#9482C9',
            '德鲁伊': '#FF7D0A',
            '恶魔猎手': '#A330C9',
            '武僧': '#00FF96',
            '唤魔师': '#33937F'
        };
        return colors[className] || '#999999';
    }

    getClassIconPath(className) {
        const classIcons = {
            '战士': 'warrior.png',
            '法师': 'mage.png',
            '猎人': 'hunter.png',
            '圣骑士': 'paladin.png',
            '牧师': 'priest.png',
            '潜行者': 'rogue.png',
            '死亡骑士': 'death-knight.png',
            '萨满祭司': 'shaman.png',
            '术士': 'warlock.png',
            '德鲁伊': 'druid.png',
            '恶魔猎手': 'demon-hunter.png',
            '武僧': 'monk.png',
            '唤魔师': 'evoker.png'
        };
        return classIcons[className] || 'warrior.png';
    }

    getFactionIconPath(faction) {
        const factionIcons = {
            'Horde': 'horde.png',
            'Alliance': 'alliance.png'
        };
        return factionIcons[faction] || 'neutral.png';
    }
    
    formatLastOnline(days) {
        if (!days || days === 0) return '<span style="color: #4CAF50;">在线</span>';
        if (days < 1) return '<span style="color: #4CAF50;">今天</span>';
        if (days < 7) return `<span style="color: #FFC107;">${Math.floor(days)}天前</span>`;
        if (days < 30) return `<span style="color: #FF9800;">${Math.floor(days / 7)}周前</span>`;
        return `<span style="color: #F44336;">${Math.floor(days / 30)}个月前</span>`;
    }
    
    renderPagination() {
        const totalPages = Math.ceil(this.filteredMembers.length / this.pageSize);
        const container = document.getElementById('pagination-container');
        const pageInfo = document.getElementById('page-info');
        const prevBtn = document.getElementById('prev-page');
        const nextBtn = document.getElementById('next-page');
        
        if (totalPages <= 1) {
            container.style.display = 'none';
            return;
        }
        
        container.style.display = 'block';
        pageInfo.textContent = `第 ${this.currentPage} 页，共 ${totalPages} 页 (共 ${this.filteredMembers.length} 条记录)`;
        prevBtn.disabled = this.currentPage <= 1;
        nextBtn.disabled = this.currentPage >= totalPages;
    }
    
    updateSortIcons() {
        // 清除所有排序图标
        document.querySelectorAll('.sortable i').forEach(icon => {
            icon.className = 'fas fa-sort';
        });
        
        // 设置当前排序字段的图标
        const currentSortHeader = document.querySelector(`[data-sort="${this.sortConfig.field}"] i`);
        if (currentSortHeader) {
            currentSortHeader.className = this.sortConfig.direction === 'asc' ? 
                'fas fa-sort-up' : 'fas fa-sort-down';
        }
    }
    
    handleSort(field) {
        if (this.sortConfig.field === field) {
            // 切换排序方向
            this.sortConfig.direction = this.sortConfig.direction === 'asc' ? 'desc' : 'asc';
        } else {
            // 新的排序字段，默认为升序
            this.sortConfig.field = field;
            this.sortConfig.direction = 'asc';
        }
        
        this.updateSortIcons();
        this.sortMembers();
        this.currentPage = 1;
        this.renderMembers();
        this.renderPagination();
    }
    
    resetFilters() {
        this.currentFilters = {
            search: '',
            class: '',
            realm: '',
            faction: ''
        };
        
        // 重置表单
        document.getElementById('search-input').value = '';
        document.getElementById('class-filter').value = '';
        document.getElementById('realm-filter').value = '';
        document.getElementById('faction-filter').value = '';
        
        this.applyFilters();
    }
    
    setupEventListeners() {
        // 搜索输入
        const searchInput = document.getElementById('search-input');
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.currentFilters.search = e.target.value;
                this.applyFilters();
            }, 300);
        });
        
        // 职业筛选
        const classFilter = document.getElementById('class-filter');
        classFilter.addEventListener('change', (e) => {
            this.currentFilters.class = e.target.value;
            this.applyFilters();
        });
        
        // 服务器筛选
        const realmFilter = document.getElementById('realm-filter');
        realmFilter.addEventListener('change', (e) => {
            this.currentFilters.realm = e.target.value;
            this.applyFilters();
        });
        
        // 阵营筛选
        const factionFilter = document.getElementById('faction-filter');
        factionFilter.addEventListener('change', (e) => {
            this.currentFilters.faction = e.target.value;
            this.applyFilters();
        });
        
        // 搜索按钮
        const searchBtn = document.getElementById('search-btn');
        searchBtn.addEventListener('click', () => {
            this.currentFilters.search = searchInput.value;
            this.applyFilters();
        });
        
        // 重置按钮
        const resetBtn = document.getElementById('reset-btn');
        resetBtn.addEventListener('click', () => {
            this.resetFilters();
        });
        
        // 每页显示数量
        const itemsPerPage = document.getElementById('items-per-page');
        itemsPerPage.addEventListener('change', (e) => {
            this.pageSize = parseInt(e.target.value);
            this.currentPage = 1;
            this.renderMembers();
            this.renderPagination();
        });
        
        // 排序功能
        document.querySelectorAll('.sortable').forEach(header => {
            header.addEventListener('click', () => {
                const field = header.getAttribute('data-sort');
                this.handleSort(field);
            });
        });
        
        // 分页按钮
        const prevBtn = document.getElementById('prev-page');
        const nextBtn = document.getElementById('next-page');
        
        prevBtn.addEventListener('click', () => {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.renderMembers();
                this.renderPagination();
            }
        });
        
        nextBtn.addEventListener('click', () => {
            const totalPages = Math.ceil(this.filteredMembers.length / this.pageSize);
            if (this.currentPage < totalPages) {
                this.currentPage++;
                this.renderMembers();
                this.renderPagination();
            }
        });
    }
    
    showError(message) {
        const tbody = document.getElementById('members-tbody');
        tbody.innerHTML = `
            <tr>
                <td colspan="9" class="error-message">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>${message}</p>
                    <button onclick="location.reload()" class="button">
                        <i class="fas fa-redo"></i> 重新加载
                    </button>
                </td>
            </tr>
        `;
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new GuildMembersPage();
}); 