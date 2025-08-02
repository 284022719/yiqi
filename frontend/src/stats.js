class GuildStats {
    constructor() {
        this.statsData = null;
        this.extendedStatsData = null;
        this.init();
        
        // 职业颜色配置 - 基于官方classcolor文件
        this.classColors = {
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
    }

    async init() {
        try {
            await this.loadStats();
            this.renderStats();
        } catch (error) {
            console.error('加载统计数据失败:', error);
            this.showError();
        }
    }

    async loadStats() {
        // 优先加载数据库统计数据
        try {
            const dbStatsResponse = await fetch('./data/database_stats.json');
            if (dbStatsResponse.ok) {
                this.statsData = await dbStatsResponse.json();
                console.log('成功加载数据库统计数据');
                
                // 尝试加载增强统计数据
                try {
                    const enhancedStatsResponse = await fetch('./data/enhanced_stats_20250801_054917.json');
                    if (enhancedStatsResponse.ok) {
                        this.enhancedStatsData = await enhancedStatsResponse.json();
                        console.log('成功加载增强统计数据');
                    }
                } catch (error) {
                    console.warn('增强统计数据加载失败:', error);
                }
                
                return;
            }
        } catch (error) {
            console.warn('数据库统计数据加载失败:', error);
        }
        
        // 如果数据库统计数据不存在，则加载会员信息统计数据
        try {
            const memberinfoResponse = await fetch('./data/memberinfo_stats.json');
            if (memberinfoResponse.ok) {
                this.statsData = await memberinfoResponse.json();
                console.log('成功加载会员信息统计数据');
                return;
            }
        } catch (error) {
            console.warn('会员信息统计数据加载失败:', error);
        }
        
        // 如果会员信息数据不存在，则加载原有数据
        const response = await fetch('./data/recent_stats.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.statsData = await response.json();
        
        try {
            const extendedResponse = await fetch('./data/extended_stats.json');
            if (extendedResponse.ok) {
                this.extendedStatsData = await extendedResponse.json();
            }
        } catch (error) {
            console.warn('扩展统计数据加载失败:', error);
            this.extendedStatsData = null;
        }
    }

    renderStats() {
        if (!this.statsData) {
            this.showError();
            return;
        }

        this.renderSummary();
        this.renderClassDistribution();
        this.renderServerDistribution();
        this.renderRaceDistribution();
        this.renderGenderDistribution();
        this.renderFactionDistribution();
        this.renderMythicRanking();
        
        // 即使 extendedStatsData 为空，也尝试渲染成就和坐骑排行
        this.renderAchievementRanking();
        this.renderMountsRanking();
    }

    renderSummary() {
        // 总会员数
        const totalMembers = document.getElementById('total-members');
        if (totalMembers && this.statsData) {
            const total = this.statsData.total_members || this.statsData.total_roles;
            if (total !== undefined) {
                totalMembers.textContent = total.toLocaleString();
            } else {
                totalMembers.textContent = '-';
            }
        }
        
        // 活跃会员数
        const activeMembers = document.getElementById('active-members');
        if (activeMembers && this.statsData) {
            const active = this.statsData.active_members;
            if (active !== undefined) {
                activeMembers.textContent = active.toLocaleString();
            } else {
                activeMembers.textContent = '-';
            }
        }
        
        // 职业种类数量
        const classCount = document.getElementById('class-count');
        if (classCount && this.statsData && this.statsData.class_distribution) {
            const count = Object.keys(this.statsData.class_distribution).length;
            classCount.textContent = count;
        } else if (classCount) {
            classCount.textContent = '-';
        }
        
        // 向后兼容：保持原有的total-roles元素
        const totalRoles = document.getElementById('total-roles');
        if (totalRoles && this.statsData) {
            const active = this.statsData.active_members || this.statsData.total_members || this.statsData.total_roles;
            if (active !== undefined) {
                totalRoles.textContent = active.toLocaleString();
            } else {
                totalRoles.textContent = '-';
            }
        }
    }

    renderClassDistribution() {
        const container = document.getElementById('class-distribution');
        if (!container || !this.statsData || !this.statsData.class_distribution) {
            if (container) {
                container.innerHTML = '<div class="error">暂无职业数据</div>';
            }
            return;
        }

        // 使用构造函数中定义的职业颜色
        const classColors = this.classColors;

        const classIcons = {
            '战士': './img/class-icons/warrior.png',
            '圣骑士': './img/class-icons/paladin.png',
            '猎人': './img/class-icons/hunter.png',
            '潜行者': './img/class-icons/rogue.png',
            '牧师': './img/class-icons/priest.png',
            '死亡骑士': './img/class-icons/death-knight.png',
            '萨满祭司': './img/class-icons/shaman.png',
            '法师': './img/class-icons/mage.png',
            '术士': './img/class-icons/warlock.png',
            '武僧': './img/class-icons/monk.png',
            '德鲁伊': './img/class-icons/druid.png',
            '恶魔猎手': './img/class-icons/demon-hunter.png',
            '唤魔师': './img/class-icons/evoker.png'
        };

        const sortedClasses = Object.entries(this.statsData.class_distribution)
            .sort((a, b) => b[1] - a[1]); // 按数量降序排列
        
        const totalMembers = Object.values(this.statsData.class_distribution).reduce((sum, count) => sum + count, 0);
        const maxCount = Math.max(...Object.values(this.statsData.class_distribution));
        
        container.innerHTML = '';
        
        sortedClasses.forEach(([className, count]) => {
                const percentage = (count / maxCount * 100).toFixed(1);
                const totalPercentage = ((count / totalMembers) * 100).toFixed(1);
                const classColor = classColors[className] || '#FFFFFF';
                const classIcon = classIcons[className] || '⚔️';
                
                const item = document.createElement('div');
                item.className = 'chart-item';
                item.innerHTML = `
                    <div class="chart-label-container">
                        <img class="class-icon" src="${classIcon}" alt="${className}" onerror="this.style.display='none'">
                        <span class="chart-label" style="color: ${classColor};">${className}</span>
                    </div>
                    <div class="chart-bar">
                        <div class="chart-bar-fill" style="width: ${percentage}%; background: ${classColor};"></div>
                    </div>
                    <span class="chart-value">${count} (${totalPercentage}%)</span>
                `;
                
                container.appendChild(item);
            });
    }

    renderServerDistribution() {
        const container = document.getElementById('server-distribution');
        if (!container || !this.statsData || !this.statsData.server_distribution) {
            if (container) {
                container.innerHTML = '<div class="error">暂无服务器数据</div>';
            }
            return;
        }

        const filteredServers = Object.entries(this.statsData.server_distribution)
            .filter(([serverName, count]) => count > 0)
            .sort((a, b) => b[1] - a[1]);

        if (filteredServers.length === 0) {
            container.innerHTML = '<div class="error">暂无服务器数据</div>';
            return;
        }
        
        container.innerHTML = '';
        
        const totalMembers = Object.values(this.statsData.server_distribution).reduce((sum, count) => sum + count, 0);
        const maxCount = Math.max(...filteredServers.map(([_, count]) => count));
        
        filteredServers
            .slice(0, 10) // 只显示前10个服务器
            .forEach(([serverName, count], index) => {
                const percentage = (count / maxCount * 100).toFixed(1);
                const totalPercentage = ((count / totalMembers) * 100).toFixed(1);
                
                const item = document.createElement('div');
                item.className = 'chart-item';
                item.innerHTML = `
                    <span class="ranking-rank">#${index + 1}</span>
                    <div class="chart-label-container">
                        <span class="chart-label">${serverName}</span>
                    </div>
                    <div class="chart-bar">
                        <div class="chart-bar-fill" style="width: ${percentage}%; background: linear-gradient(90deg, #FF6B6B, #C44569);"></div>
                    </div>
                    <span class="chart-value">${count} (${totalPercentage}%)</span>
                `;
                
                container.appendChild(item);
            });
    }

    renderRaceDistribution() {
        const container = document.getElementById('race-distribution');
        if (!container) {
            return;
        }

        // 优先使用会员信息数据中的种族分布
        let raceDistribution = {};
        if (this.statsData && this.statsData.race_distribution) {
            raceDistribution = this.statsData.race_distribution;
        } else if (this.extendedStatsData && this.extendedStatsData.race_distribution) {
            raceDistribution = this.extendedStatsData.race_distribution;
        }

        if (Object.keys(raceDistribution).length === 0) {
            container.innerHTML = '<div class="error">暂无种族数据</div>';
            return;
        }

        const sortedRaces = Object.entries(raceDistribution)
            .sort((a, b) => b[1] - a[1]);
        
        if (sortedRaces.length === 0) {
            container.innerHTML = '<div class="error">暂无种族数据</div>';
            return;
        }
        
        container.innerHTML = '';
        
        const totalMembers = Object.values(raceDistribution).reduce((sum, count) => sum + count, 0);
        const maxCount = Math.max(...sortedRaces.map(([_, count]) => count));
        
        sortedRaces
            .slice(0, 10) // 只显示前10个种族
            .forEach(([raceName, count], index) => {
                const percentage = (count / maxCount * 100).toFixed(1);
                const totalPercentage = ((count / totalMembers) * 100).toFixed(1);
                
                const item = document.createElement('div');
                item.className = 'chart-item';
                item.innerHTML = `
                    <span class="ranking-rank">#${index + 1}</span>
                    <div class="chart-label-container">
                        <span class="chart-label">${raceName}</span>
                    </div>
                    <div class="chart-bar">
                        <div class="chart-bar-fill" style="width: ${percentage}%; background: linear-gradient(90deg, #4ECDC4, #44A08D);"></div>
                    </div>
                    <span class="chart-value">${count} (${totalPercentage}%)</span>
                `;
                
                container.appendChild(item);
            });
    }

    renderGenderDistribution() {
        const container = document.getElementById('gender-distribution');
        if (!container) {
            return;
        }

        // 优先使用会员信息数据中的性别分布
        let data = {};
        if (this.statsData && this.statsData.gender_distribution) {
            data = this.statsData.gender_distribution;
        } else if (this.extendedStatsData && this.extendedStatsData.gender_distribution) {
            data = this.extendedStatsData.gender_distribution;
        }

        if (Object.keys(data).length === 0) {
            container.innerHTML = '<div class="error">暂无性别数据</div>';
            return;
        }
        const total = Object.values(data).reduce((sum, count) => sum + count, 0);
        
        if (total === 0) {
            container.innerHTML = '<div class="error">暂无性别数据</div>';
            return;
        }
        
        container.innerHTML = '';
        
        const pieContainer = document.createElement('div');
        pieContainer.className = 'pie-container';
        
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('width', '220');
        svg.setAttribute('height', '220');
        svg.setAttribute('viewBox', '0 0 220 220');
        
        const centerX = 110;
        const centerY = 110;
        const radius = 80;
        
        let currentAngle = 0;
        const colors = ['#FF6B6B', '#4ECDC4'];
        
        Object.entries(data).forEach(([gender, count], index) => {
            const percentage = count / total;
            const angle = percentage * 360;
            const genderText = gender === 'Male' ? '男性' : 
                              gender === 'Female' ? '女性' : 
                              gender === '女性' ? '女性' : 
                              gender === '男性' ? '男性' : gender;
            
            if (percentage > 0) {
                const startAngle = currentAngle * Math.PI / 180;
                const endAngle = (currentAngle + angle) * Math.PI / 180;
                
                const x1 = centerX + radius * Math.cos(startAngle);
                const y1 = centerY + radius * Math.sin(startAngle);
                const x2 = centerX + radius * Math.cos(endAngle);
                const y2 = centerY + radius * Math.sin(endAngle);
                
                const largeArcFlag = angle > 180 ? 1 : 0;
                const pathData = [
                    `M ${centerX} ${centerY}`,
                    `L ${x1} ${y1}`,
                    `A ${radius} ${radius} 0 ${largeArcFlag} 1 ${x2} ${y2}`,
                    'Z'
                ].join(' ');
                
                const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                path.setAttribute('d', pathData);
                path.setAttribute('fill', colors[index % colors.length]);
                path.setAttribute('stroke', '#fff');
                path.setAttribute('stroke-width', '2');
                path.style.transition = 'all 0.3s ease';
                
                path.addEventListener('mouseenter', () => {
                    path.style.filter = 'brightness(1.2)';
                    path.style.transform = 'scale(1.05)';
                });
                
                path.addEventListener('mouseleave', () => {
                    path.style.filter = 'none';
                    path.style.transform = 'scale(1)';
                });
                
                svg.appendChild(path);
            }
            
            currentAngle += angle;
        });
        
        pieContainer.appendChild(svg);
        
        const legend = document.createElement('div');
        legend.className = 'pie-legend';
        
        Object.entries(data).forEach(([gender, count], index) => {
            const percentage = (count / total * 100).toFixed(1);
            const genderText = gender === 'Male' ? '男性' : 
                              gender === 'Female' ? '女性' : 
                              gender === '女性' ? '女性' : 
                              gender === '男性' ? '男性' : gender;
            
            const legendItem = document.createElement('div');
            legendItem.className = 'legend-item';
            legendItem.innerHTML = `
                <div class="legend-color" style="background: ${colors[index % colors.length]}"></div>
                <span class="legend-text">${genderText}</span>
                <span class="legend-value">${count} (${percentage}%)</span>
            `;
            legend.appendChild(legendItem);
        });
        
        container.appendChild(pieContainer);
        container.appendChild(legend);
    }

    renderFactionDistribution() {
        const container = document.getElementById('faction-distribution');
        if (!container) {
            return;
        }

        // 优先使用会员信息数据中的阵营分布
        let data = {};
        if (this.statsData && this.statsData.faction_distribution) {
            data = this.statsData.faction_distribution;
        } else if (this.extendedStatsData && this.extendedStatsData.faction_distribution) {
            data = this.extendedStatsData.faction_distribution;
        }

        if (Object.keys(data).length === 0) {
            container.innerHTML = '<div class="error">暂无阵营数据</div>';
            return;
        }
        const total = Object.values(data).reduce((sum, count) => sum + count, 0);
        
        if (total === 0) {
            container.innerHTML = '<div class="error">暂无阵营数据</div>';
            return;
        }
        
        container.innerHTML = '';
        
        const pieContainer = document.createElement('div');
        pieContainer.className = 'pie-container';
        
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('width', '220');
        svg.setAttribute('height', '220');
        svg.setAttribute('viewBox', '0 0 220 220');
        
        const centerX = 110;
        const centerY = 110;
        const radius = 80;
        
        let currentAngle = 0;
        const factionConfig = {
            'Horde': {
                text: '部落',
                color: '#8B0000',
                icon: './img/faction-icons/horde.png'
            },
            'Alliance': {
                text: '联盟',
                color: '#00008B',
                icon: './img/faction-icons/alliance.png'
            },
            '部落': {
                text: '部落',
                color: '#8B0000',
                icon: './img/faction-icons/horde.png'
            },
            '联盟': {
                text: '联盟',
                color: '#00008B',
                icon: './img/faction-icons/alliance.png'
            }
        };
        
        Object.entries(data).forEach(([faction, count], index) => {
            const percentage = count / total;
            const angle = percentage * 360;
            const config = factionConfig[faction];
            
            // 如果找不到配置，跳过这个阵营
            if (!config) {
                console.warn(`未找到阵营配置: ${faction}`);
                return;
            }
            
            if (percentage > 0) {
                const startAngle = currentAngle * Math.PI / 180;
                const endAngle = (currentAngle + angle) * Math.PI / 180;
                
                const x1 = centerX + radius * Math.cos(startAngle);
                const y1 = centerY + radius * Math.sin(startAngle);
                const x2 = centerX + radius * Math.cos(endAngle);
                const y2 = centerY + radius * Math.sin(endAngle);
                
                const largeArcFlag = angle > 180 ? 1 : 0;
                const pathData = [
                    `M ${centerX} ${centerY}`,
                    `L ${x1} ${y1}`,
                    `A ${radius} ${radius} 0 ${largeArcFlag} 1 ${x2} ${y2}`,
                    'Z'
                ].join(' ');
                
                const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                path.setAttribute('d', pathData);
                path.setAttribute('fill', config.color);
                path.setAttribute('stroke', '#fff');
                path.setAttribute('stroke-width', '2');
                path.style.transition = 'all 0.3s ease';
                
                path.addEventListener('mouseenter', () => {
                    path.style.filter = 'brightness(1.2)';
                    path.style.transform = 'scale(1.05)';
                });
                
                path.addEventListener('mouseleave', () => {
                    path.style.filter = 'none';
                    path.style.transform = 'scale(1)';
                });
                
                svg.appendChild(path);
            }
            
            currentAngle += angle;
        });
        
        pieContainer.appendChild(svg);
        
        const legend = document.createElement('div');
        legend.className = 'pie-legend';
        
        Object.entries(data).forEach(([faction, count], index) => {
            const percentage = (count / total * 100).toFixed(1);
            const config = factionConfig[faction];
            
            // 如果找不到配置，跳过这个阵营
            if (!config) {
                console.warn(`未找到阵营配置: ${faction}`);
                return;
            }
            
            const legendItem = document.createElement('div');
            legendItem.className = 'legend-item';
            legendItem.innerHTML = `
                <img class="faction-icon" src="${config.icon}" alt="${config.text}" onerror="this.style.display='none'">
                <div class="legend-color" style="background: ${config.color}"></div>
                <span class="legend-text">${config.text}</span>
                <span class="legend-value">${count} (${percentage}%)</span>
            `;
            legend.appendChild(legendItem);
        });
        
        container.appendChild(pieContainer);
        container.appendChild(legend);
    }

    renderMythicRanking() {
        const container = document.getElementById('mythic-ranking');
        if (!container) {
            return;
        }

        // 使用构造函数中定义的职业颜色
        const classColors = this.classColors;

        // 优先使用增强统计数据中的 Mythic+ 排行
        let mythicData = [];
        if (this.enhancedStatsData && this.enhancedStatsData.mythic_ranking) {
            mythicData = this.enhancedStatsData.mythic_ranking.slice(0, 10);
        } else if (this.statsData && this.statsData.mythic_ranking) {
            mythicData = this.statsData.mythic_ranking.slice(0, 10);
        } else if (this.extendedStatsData && this.extendedStatsData.mythic_ranking) {
            mythicData = this.extendedStatsData.mythic_ranking.slice(0, 10);
        }

        if (mythicData.length === 0) {
            container.innerHTML = '<div class="error">暂无 Mythic+ 数据</div>';
            return;
        }

        container.innerHTML = '';
        
        mythicData.forEach((role, index) => {
                const item = document.createElement('div');
                item.className = 'ranking-item';
                
                if (index === 0) {
                    item.classList.add('legendary-item');
                } else if (index === 1) {
                    item.classList.add('epic-item');
                } else if (index === 2) {
                    item.classList.add('rare-item');
                } else if (index === 3) {
                    item.classList.add('uncommon-item');
                }
                
                // 获取职业颜色
                const classColor = classColors[role.class] || '#FFFFFF';
                
                item.innerHTML = `
                    <span class="ranking-rank">#${index + 1}</span>
                    <div class="ranking-info">
                        <div class="ranking-name" style="color: ${classColor};">${role.name}</div>
                        <div class="ranking-class">${role.class}</div>
                    </div>
                    <span class="ranking-score">${role.mythic_score}</span>
                `;
                
                container.appendChild(item);
            });
    }

    renderAchievementRanking() {
        const container = document.getElementById('achievement-ranking');
        if (!container) {
            return;
        }

        // 使用构造函数中定义的职业颜色
        const classColors = this.classColors;

        // 优先使用增强统计数据中的成就排行
        let achievementData = [];
        if (this.enhancedStatsData && this.enhancedStatsData.achievement_ranking) {
            achievementData = this.enhancedStatsData.achievement_ranking.slice(0, 10);
        } else if (this.statsData && this.statsData.recent_roles) {
            achievementData = this.statsData.recent_roles
                .filter(role => role.achievement_points)
                .sort((a, b) => b.achievement_points - a.achievement_points)
                .slice(0, 10);
        } else if (this.extendedStatsData && this.extendedStatsData.achievement_ranking) {
            achievementData = this.extendedStatsData.achievement_ranking.slice(0, 10);
        }

        if (achievementData.length === 0) {
            container.innerHTML = '<div class="error">暂无成就数据</div>';
            return;
        }

        container.innerHTML = '';
        
        achievementData.forEach((role, index) => {
                const item = document.createElement('div');
                item.className = 'ranking-item';
                
                if (index === 0) {
                    item.classList.add('legendary-item');
                } else if (index === 1) {
                    item.classList.add('epic-item');
                } else if (index === 2) {
                    item.classList.add('rare-item');
                } else if (index === 3) {
                    item.classList.add('uncommon-item');
                }
                
                // 获取职业颜色
                const classColor = classColors[role.class] || '#FFFFFF';
                
                item.innerHTML = `
                    <span class="ranking-rank">#${index + 1}</span>
                    <div class="ranking-info">
                        <div class="ranking-name" style="color: ${classColor};">${role.name}</div>
                        <div class="ranking-class">${role.class}</div>
                    </div>
                    <span class="ranking-score">${role.achievement_points}</span>
                `;
                
                container.appendChild(item);
            });
    }

    renderMountsRanking() {
        const container = document.getElementById('mounts-ranking');
        if (!container) {
            return;
        }

        // 使用构造函数中定义的职业颜色
        const classColors = this.classColors;

        // 优先使用增强统计数据中的坐骑排行
        let mountsData = [];
        if (this.enhancedStatsData && this.enhancedStatsData.mounts_ranking) {
            mountsData = this.enhancedStatsData.mounts_ranking.slice(0, 10);
        } else if (this.statsData && this.statsData.mounts_ranking) {
            mountsData = this.statsData.mounts_ranking.slice(0, 10);
        } else if (this.extendedStatsData && this.extendedStatsData.mounts_ranking) {
            mountsData = this.extendedStatsData.mounts_ranking.slice(0, 10);
        }

        if (mountsData.length === 0) {
            container.innerHTML = '<div class="error">暂无坐骑数据</div>';
            return;
        }

        container.innerHTML = '';
        
        mountsData.forEach((role, index) => {
                const item = document.createElement('div');
                item.className = 'ranking-item';
                
                if (index === 0) {
                    item.classList.add('legendary-item');
                } else if (index === 1) {
                    item.classList.add('epic-item');
                } else if (index === 2) {
                    item.classList.add('rare-item');
                } else if (index === 3) {
                    item.classList.add('uncommon-item');
                }
                
                // 获取职业颜色
                const classColor = classColors[role.class] || '#FFFFFF';
                
                item.innerHTML = `
                    <span class="ranking-rank">#${index + 1}</span>
                    <div class="ranking-info">
                        <div class="ranking-name" style="color: ${classColor};">${role.name}</div>
                        <div class="ranking-class">${role.class}</div>
                    </div>
                    <span class="ranking-score">${role.mounts_count}</span>
                `;
                
                container.appendChild(item);
            });
    }

    showError() {
        const containers = ['class-distribution', 'server-distribution', 'race-distribution', 'gender-distribution', 'faction-distribution', 'mythic-ranking', 'achievement-ranking', 'mounts-ranking'];
        containers.forEach(id => {
            const container = document.getElementById(id);
            if (container) {
                container.innerHTML = '<div class="error">加载统计数据失败</div>';
            }
        });
    }
}

// ES6模块导出
export { GuildStats };

// 为了向后兼容，也添加到全局对象
if (typeof window !== 'undefined') {
    window.GuildStats = GuildStats;
}

// 自动初始化（如果不在模块环境中）
if (typeof window !== 'undefined' && !window.GuildStats) {
    new GuildStats();
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('guild-stats')) {
        new GuildStats();
    }
}); 