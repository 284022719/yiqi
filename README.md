# 一起公会 · 站点

魔兽世界「一起」公会的静态站点：首页统计、职业天梯、开荒记录、公会画廊与战术攻略。

- 前端：原生 ES Modules + 多文件 CSS，无构建步骤
- 后端：Netlify Functions（WCL 代理、Cloudinary 图床）
- 数据：Python 离线管道抓取 → SQLite → 生成 `data/page_data.json`

详细设计见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) 与 [docs/DATA_PIPELINE.md](docs/DATA_PIPELINE.md)。

## 目录

```
index.html              首页（统计图表 + 排行榜）
pages/                  子页面：职业天梯、画廊、开荒记录、攻略、配色预览
css/                    样式（main.css 通过 @import 组合）
js/
  main.js               入口：按页面元素条件初始化
  config.js             全局配置与错误处理
  core/                 通用工具（HTML 转义等）
  data/                 静态数据与配色表（wow-classes / specs / tier-lists / palettes）
  components/           可复用 UI（TierList / Chart / 导航 / Header / Footer）
  modules/              页面级控制器（统计、WCL、画廊、灯箱、粒子）
netlify/functions/      服务端函数（CommonJS）
tools/                  Python 数据管道与校验
data/                   生成产物与本地数据库（数据库不入库）
```

## 本地预览

只预览静态页面：

```bash
python -m http.server 8080
# 打开 http://localhost:8080/
```

需要联调 Netlify Functions（画廊上传、WCL 拉取）时必须用 Netlify CLI：

```bash
npm install -g netlify-cli
netlify dev
```

> 直接用 `http.server` 时，`/.netlify/functions/*` 会 404，属预期现象。

## 数据管道

```bash
python tools/build_page_data.py     # 读取 SQLite，生成 data/page_data.json
python tools/validate.py            # 校验产物（结构与合理性断言）
python tools/validate.py --strict   # 数据过期也视为失败，适合 CI
```

活跃口径可用环境变量调整（默认 30 天）：

```bash
ACTIVE_DAYS=14 python tools/build_page_data.py
```

注意：数据库与配置文件**不在版本库中**，需要另行获取；缺失时脚本会给出明确提示。

## 环境变量

在 Netlify 站点设置中配置（本地可放 `.env`，已被忽略）：

| 变量 | 用途 | 必填 |
|---|---|---|
| `WCL_CLIENT_ID` / `WCL_CLIENT_SECRET` | WarcraftLogs OAuth | 是（开荒记录页） |
| `CLOUDINARY_CLOUD_NAME` / `CLOUDINARY_API_KEY` / `CLOUDINARY_API_SECRET` | 画廊图床 | 是（画廊页） |
| `UPLOAD_TOKEN` | 上传口令；**设置后**上传接口才要求鉴权 | 否 |

> 暴雪 API 令牌外置尚未完成（历史上硬编码在 `data/config.json` 与 `tools/config.py` 中），见 [docs/DATA_PIPELINE.md](docs/DATA_PIPELINE.md#待办)。

## 开发约定

1. **颜色只有一份来源**：`css/variables.css` 的 `--class-*`；JS 里用 `resolveClassColor()`，不要新增色表。
2. **样式写在 `css/` 下**，不要在 JS 里 `createElement('style')` 注入。
3. **拼接 HTML 必须转义**：使用 `js/core/dom.js` 的 `escapeHtml` / `escapeAttr`。
4. **调试日志用 `log()`**（`js/config.js`），默认关闭；不要直接留 `console.log`。
5. **天梯数据只改 `js/data/specs.js`**（专精图标）与 `js/data/*-tier-list.js`（排名 id 列表）。
6. **不要手改 `data/page_data.json`**，它由 `tools/build_page_data.py` 生成。

## 代码检查

```bash
npm install
npm run lint          # ESLint（js/ 与 netlify/functions/）
npm run format:check  # Prettier 检查
```

> `package-lock.json` 尚未包含新增的 devDependencies，首次安装会由 `npm install` 自动补全；在此之前请勿使用 `npm ci`。
>
> 历史文件未按 Prettier 统一格式化，首次使用请先执行一次 `npm run format`，之后再以 `npm run format:check` 作为门禁。

## 部署

推送到 `main` 分支后由 Netlify 自动构建；`netlify.toml` 已声明发布目录、函数目录、Node 版本、安全响应头与缓存策略。
