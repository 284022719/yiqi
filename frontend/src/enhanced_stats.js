/**
 * 增强版统计组件
 * 展示装备、成就、副本进度等详细游戏数据
 */

class EnhancedStats {
    constructor() {
        this.enhancedData = null;
        this.init();
    }

    async init() {
        try {
            await this.loadEnhancedData();
            this.renderEnhancedStats();
        } catch (error) {
            console.error('加载增强统计数据失败:', error);
            this.showError();
        }
    }

    async loadEnhancedData() {
        try {
            // 尝试加载最新的增强数据
            const response = await fetch('./data/enhanced_api_results_latest.json');
            if (response.ok) {
                this.enhancedData = await response.json();
                console.log('成功加载增强统计数据');
                return;
            }
        } catch (error) {
            console.warn('增强统计数据加载失败:', error);
        }
        
        // 如果没有增强数据，使用基础数据
        this.enhancedData = null;
    }

    renderEnhancedStats() {
        if (!this.enhancedData) {
            this.showError();
            return;
        }

        this.renderEquipmentStats();
        this.renderAchievementStats();
        this.renderRaidStats();

    }

    renderEquipmentStats() {
        const container = document.getElementById('equipment-stats');
        if (!container) return;

        const equipmentData = this.enhancedData.filter(item => 
            item.status === 'success' && item.data && item.data.equipment
        );

        if (equipmentData.length === 0) {
            container.innerHTML = '<div class="error">暂无装备数据</div>';
            return;
        }

        // 统计装备等级
        const itemLevels = equipmentData.map(item => {
            const char = item.data.character_summary;
            return {
                name: char.name,
                class: char.character_class.name,
                itemLevel: char.average_item_level,
                equippedItemLevel: char.equipped_item_level
            };
        }).sort((a, b) => b.itemLevel - a.itemLevel);

        container.innerHTML = `
            <h3>⚔️ 装备等级排行</h3>
            <div class="equipment-ranking">
                ${itemLevels.slice(0, 10).map((char, index) => `
                    <div class="ranking-item ${this.getRankingClass(index)}">
                        <span class="ranking-rank">#${index + 1}</span>
                        <div class="ranking-info">
                            <div class="ranking-name" style="color: ${this.getClassColor(char.class)};">${char.name}</div>
                            <div class="ranking-class">${char.class}</div>
                        </div>
                        <div class="ranking-scores">
                            <span class="item-level">${char.itemLevel}</span>
                            <span class="equipped-level">(${char.equippedItemLevel})</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    renderAchievementStats() {
        const container = document.getElementById('achievement-stats');
        if (!container) return;

        const achievementData = this.enhancedData.filter(item => 
            item.status === 'success' && item.data && item.data.character_summary
        );

        if (achievementData.length === 0) {
            container.innerHTML = '<div class="error">暂无成就数据</div>';
            return;
        }

        // 统计成就点数
        const achievements = achievementData.map(item => {
            const char = item.data.character_summary;
            return {
                name: char.name,
                class: char.character_class.name,
                achievementPoints: char.achievement_points
            };
        }).sort((a, b) => b.achievementPoints - a.achievementPoints);

        container.innerHTML = `
            <h3>🏆 成就点数排行</h3>
            <div class="achievement-ranking">
                ${achievements.slice(0, 10).map((char, index) => `
                    <div class="ranking-item ${this.getRankingClass(index)}">
                        <span class="ranking-rank">#${index + 1}</span>
                        <div class="ranking-info">
                            <div class="ranking-name" style="color: ${this.getClassColor(char.class)};">${char.name}</div>
                            <div class="ranking-class">${char.class}</div>
                        </div>
                        <span class="ranking-score">${char.achievementPoints.toLocaleString()}</span>
                    </div>
                `).join('')}
            </div>
        `;
    }

    renderRaidStats() {
        const container = document.getElementById('raid-stats');
        if (!container) return;

        // 这里可以添加副本进度统计
        container.innerHTML = `
            <h3>🏰 副本进度</h3>
            <div class="raid-progress">
                <div class="info-note">副本进度数据正在开发中...</div>
            </div>
        `;
    }

    

    getClassColor(className) {
        const classColors = {
            '战士': '#C69B6D',
            '圣骑士': '#F48CBA',
            '猎人': '#AAD372',
            '潜行者': '#FFF468',
            '牧师': '#FFFFFF',
            '死亡骑士': '#C41E3A',
            '萨满祭司': '#0070DD',
            '法师': '#3FC7EB',
            '术士': '#8788EE',
            '武僧': '#00FF98',
            '德鲁伊': '#FF7C0A',
            '恶魔猎手': '#A330C9',
            '唤魔师': '#33937F'
        };
        return classColors[className] || '#FFFFFF';
    }

    getRankingClass(index) {
        if (index === 0) return 'legendary-item';
        if (index === 1) return 'epic-item';
        if (index === 2) return 'rare-item';
        if (index === 3) return 'uncommon-item';
        return '';
    }

    showError() {
        const containers = ['equipment-stats', 'achievement-stats', 'raid-stats'];
        containers.forEach(id => {
            const container = document.getElementById(id);
            if (container) {
                container.innerHTML = '<div class="error">加载增强统计数据失败</div>';
            }
        });
    }
}

// 当DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('enhanced-stats-container')) {
        new EnhancedStats();
    }
}); 