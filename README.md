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
| `WOW_ARMORY_TOKEN` | 暴雪国服 armory 令牌（Python 数据管道用，不参与建站） | 否（只有跑爬虫/令牌测试时需要） |

> 暴雪 API 令牌已经外置：仓库里不再有任何令牌，`tools/config.py` 优先读 `WOW_ARMORY_TOKEN`，
> 其次读 `tools/config.json`（已 gitignore；示例见 `tools/config.example.json`）。
> 网站本身不依赖这个令牌——静态页面只读 `data/page_data.json`。

## 开发约定

1. **颜色只有一份来源**：`css/variables.css` 的 `--class-*`；JS 里用 `resolveClassColor()`，不要新增色表。
2. **样式写在 `css/` 下**，不要在 JS 里 `createElement('style')` 注入。
3. **拼接 HTML 必须转义**：使用 `js/core/dom.js` 的 `escapeHtml` / `escapeAttr`。
4. **调试日志用 `log()`**（`js/config.js`），默认关闭；不要直接留 `console.log`。
5. **天梯数据只改 `js/data/specs.js`**（专精图标）与 `js/data/*-tier-list.js`（排名 id 列表）。
6. **不要手改 `data/page_data.json`**，它由 `tools/build_page_data.py` 生成。

## 测试

测试**只用标准库**（Node 的 `node:test` + Python 的 `unittest`），不需要 `npm install` 就能跑：

```bash
npm test          # JS + Python 全部
npm run test:js   # node --test（自动发现 tests/js/*.test.mjs）
npm run test:py   # python -m unittest discover -s tests/py
npm run check     # 测试 + 页面数据校验
```

没有 Node/npm 时的等价命令：

```bash
node --test
python -m unittest discover -s tests/py -p "test_*.py"
```

覆盖范围：

| 文件 | 覆盖内容 |
|---|---|
| `tests/js/dom.test.mjs` | HTML 转义（防注入）、`byId` 的安全降级 |
| `tests/js/icons.test.mjs` | 图标集生成、不再混入 emoji |
| `tests/js/chart.test.mjs` | 条形图/饼图的空状态、百分比、角度累计、转义 |
| `tests/js/data.test.mjs` | 职业表查询、专精注册表、**6 份天梯的专精 id 全部可解析** |
| `tests/py/test_timeutil.py` | 毫秒/秒归一化（历史 bug 的回归保护） |
| `tests/py/test_paths.py` | 路径解析不依赖 cwd |
| `tests/py/test_stats.py` | 去重规则、活跃口径、完整率、排行榜排序 |

CI 见 `.github/workflows/ci.yml`：推送到 `main` 或开 PR 时跑上述测试 + `tools/validate.py`。

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

推送到 `main` 分支后由 Netlify 自动构建；`netlify.toml` 已声明发布目录、函数目录、Node 版本、安全响应头（含 CSP）与缓存策略。
