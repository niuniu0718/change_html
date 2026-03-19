# SCM 变更管理统计分析报表

## 本地部署说明 - 数据完全保存在公司内网

### 目录结构

```
scm-dashboard/
├── data/
│   └── source.csv          # 【你的数据放在这里】
├── app.py                   # 主程序
├── requirements.txt         # 依赖
└── README.md               # 说明文档
```

### 第一步：放置数据文件

1. 在项目目录下创建 `data` 文件夹：
   ```bash
   mkdir data
   ```

2. 将你的 Excel 数据另存为 CSV 格式：
   - Excel 中点击"另存为"
   - 选择格式：`CSV (逗号分隔) (*.csv)`
   - 命名为：`source.csv`
   - 放入 `data` 文件夹

### 第二步：安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 第三步：运行报表

```bash
streamlit run app.py
```

浏览器会自动打开到 `http://localhost:8501`

### 安全说明

| 安全措施 | 说明 |
|---------|------|
| 本地运行 | 服务只绑定 `127.0.0.1`，外网无法访问 |
| 数据不出内网 | 所有数据文件都在本地，不上传任何云端 |
| 关闭服务即停止 | 终端 Ctrl+C 停止服务后，无法访问数据 |

### 常用功能

- **侧边栏筛选**：按日期、类型、等级、状态、主导人筛选
- **关键指标**：总单量、进行中、已完成、关键件变更、一级变更
- **趋势分析**：按日查看变更数量趋势
- **TOP 分析**：供应商、主导人、变更原因等排行
- **数据导出**：在页面底部可导出当前筛选后的数据

### 停止服务

在运行终端按 `Ctrl + C`
