# 文档索引

| 文档 | 内容 |
|---|---|
| [../README.md](../README.md) | 项目概览、本地运行、环境变量、开发约定 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 页面与入口、JS 分层、渲染约定、数据流、取舍 |
| [DATA_PIPELINE.md](DATA_PIPELINE.md) | 数据管道命令、库表结构、统计口径、输出契约、已知数据问题 |
| [REFACTOR_PLAN.md](REFACTOR_PLAN.md) | 重构方案与验收清单（历史决策记录） |
| [wow-mounts-api.md](wow-mounts-api.md) | 暴雪坐骑 API 原始调研笔记 |

`archive/` 下为重构前的历史文档，内容已被上述文档覆盖，仅供追溯。

主题速查：

- 想改职业颜色 → `css/variables.css` 的 `--class-*`
- 想改天梯图标 → `js/data/specs.js`
- 想改天梯排名 → `js/data/*-tier-list.js`
- 想改首页统计 → `tools/build_page_data.py`
- 想改接口行为 → `netlify/functions/`
