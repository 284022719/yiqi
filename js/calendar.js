// 活动日历功能
class GuildCalendar {
  constructor() {
    this.calendarEl = document.getElementById('event-calendar');
    this.signupButton = document.getElementById('signup-button');
    this.selectedEvent = null;
    this.init();
  }
  
  async init() {
    try {
      await this.initCalendar();
      this.setupEventListeners();
    } catch (error) {
      this.showError(error);
    }
  }
  
  async initCalendar() {
    const Calendar = FullCalendar.Calendar;
    
    this.calendar = new Calendar(this.calendarEl, {
      initialView: 'dayGridMonth',
      locale: 'zh-cn',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,listWeek'
      },
      events: async (info, successCallback) => {
        try {
          const response = await fetch(`/.netlify/functions/get-events?start=${info.startStr}&end=${info.endStr}`);
          const data = await response.json();
          successCallback(data.events);
        } catch (error) {
          console.error('加载日历事件失败:', error);
          successCallback([]);
        }
      },
      eventClick: (info) => {
        this.selectedEvent = info.event;
        this.signupButton.disabled = false;
        this.signupButton.textContent = `报名: ${info.event.title}`;
      },
      eventContent: (arg) => {
        return {
          html: `
            <div class="fc-event-main">
              <i class="fas fa-${arg.event.extendedProps.icon || 'calendar-alt'}"></i>
              ${arg.event.title}
            </div>
          `
        };
      }
    });
    
    this.calendar.render();
  }
  
  setupEventListeners() {
    this.signupButton.addEventListener('click', async () => {
      if (!this.selectedEvent) return;
      
      try {
        this.signupButton.disabled = true;
        this.signupButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 报名中...';
        
        const response = await fetch('/.netlify/functions/signup-event', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            eventId: this.selectedEvent.id
          })
        });
        
        if (!response.ok) throw new Error('报名失败');
        
        const result = await response.json();
        alert(`报名成功！${result.message}`);
      } catch (error) {
        alert(`报名失败: ${error.message}`);
      } finally {
        this.signupButton.disabled = false;
        this.signupButton.textContent = `报名: ${this.selectedEvent.title}`;
      }
    });
  }
  
  showError(error) {
    this.calendarEl.innerHTML = `
      <div class="error">
        <i class="fas fa-exclamation-triangle"></i> 
        无法加载日历: ${error.message}
      </div>
    `;
  }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
  new GuildCalendar();
});
