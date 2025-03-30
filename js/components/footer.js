export function loadFooter() {
    const footerHTML = `
      <footer class="content-card">
        <address>
          <p><img src="img/yy.png" alt="YY语音" width="20" height="20"> YY：74814646</p>
          <p><img src="img/bn.webp" alt="战网" width="20" height="20"> 战网：284022719@qq.com</p>
        </address>
      </footer>
    `;
    
    document.body.insertAdjacentHTML('beforeend', footerHTML);
  }