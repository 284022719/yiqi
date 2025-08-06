export function loadFooter() {
    const footerHTML = `
      <footer class="footer-container">
        
        <div>
            <img src="https://web.yystatic.com/project/yycom_header/pc/assets/logo.png" alt="YY语音" width="24" height="24">
            <span>74814646</span>
        </div>
           
        <div>
            <img src="https://contentstack-images.blzstatic.cn/v3/assets/blt13393558c8f39060/blt99d316461099db22/644fe236d3c3ea26f40ed388/desktop-app.png" alt="战网" width="24" height="24">
            <span>284022719@qq.com</span>
        </div>

      </footer>
    `;
    
    document.body.insertAdjacentHTML('beforeend', footerHTML);
  }