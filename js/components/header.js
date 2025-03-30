export function loadHeader() {
    const headerHTML = `
      <canvas id="particle-canvas" style="position: fixed; top: 0; left: 0; z-index: -1;"></canvas>
      <header class="guild-header">
        <h1 class="guild-title">一起公会</h1>
        <p class="guild-motto">打本 休闲 洗脚</p>
      </header>
    `;
    
    document.body.insertAdjacentHTML('afterbegin', headerHTML);
  }