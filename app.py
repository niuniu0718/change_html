# -*- coding: utf-8 -*-
"""
SCM 变更管理统计分析报表
本地部署版本 - 数据不联网
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="SCM 变更管理仪表盘",
    page_icon="📊",
    layout="wide",
    menu_items={
        "About": "SCM 变更管理统计分析报表 v1.0"
    }
)

# ==================== 自定义 CSS ====================
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    .metric-card.green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .metric-card.orange {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .metric-card.blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .stDataFrame {
        font-size: 13px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 36px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 标题 ====================
st.title("📊 SCM 变更管理统计分析仪表盘")
st.markdown("---")

# ==================== 数据加载 ====================
@st.cache_data
def load_data():
    """加载本地数据 - 支持多种编码格式"""
    try:
        # 尝试多种编码格式（UTF-8、GBK、GB2312 等）
        encodings = ['utf-8-sig', 'utf-8', 'gbk', 'gb2312', 'gb18030']
        for encoding in encodings:
            try:
                df = pd.read_csv("data/source.csv", encoding=encoding)
                st.info(f"✅ 使用 {encoding} 编码成功加载数据")
                return df
            except UnicodeDecodeError:
                continue

        # 如果所有编码都失败，尝试自动检测
        import chardet
        with open("data/source.csv", 'rb') as f:
            raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            detected_encoding = result['encoding']

        df = pd.read_csv("data/source.csv", encoding=detected_encoding)
        st.info(f"✅ 使用自动检测的 {detected_encoding} 编码成功加载数据")
        return df

    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"读取数据失败：{e}")
        return None

df = load_data()

if df is None:
    st.warning("⚠️ 未找到数据文件，请将数据文件放置在 `data/source.csv`")

    if st.button("加载示例数据（演示用）"):
        np.random.seed(42)
        n_rows = 1000

        df_sample = pd.DataFrame({
            '流程单号 (BPM)': [f'SCM078-20260{np.random.randint(1,31):02d}-{np.random.randint(1,100):03d}' for _ in range(n_rows)],
            '申请日期': pd.date_range('2026-01-01', periods=n_rows, freq='H'),
            '一级变更项目': np.random.choice(['5M1E 变更', '设计变更', '工艺变更', '供应商变更', '材料变更'], n_rows),
            'SRM 单号': [f'00000000{np.random.randint(1000,9999)}' for _ in range(n_rows)],
            'CATL 设计工程师': np.random.choice(['林宋锦', '王文杰', '张三', '李四', '王五'], n_rows),
            'CATL 部 PMC-MC 工程师': np.random.choice(['王文杰', '赵六', '钱七'], n_rows),
            'CATL SQE 工程师': np.random.choice(['昊淮钰', '孙八', '周九'], n_rows),
            'CATL SRC 工程师': np.random.choice(['赵奇绘', '吴十', '郑十一'], n_rows),
            '变更触发原因分类': np.random.choice(['就近配套客户', '成本优化', '质量改善', '供应商切换', '法规要求', '设计优化'], n_rows),
            '供应商代码': [f'000000{np.random.randint(100,999)}' for _ in range(n_rows)],
            '零件重要等级': np.random.choice(['关键件', '重要件', '一般件'], n_rows, p=[0.3, 0.4, 0.3]),
            '物料类型': np.random.choice(['电芯化学料', '结构件', '电子料', '包材', '辅料'], n_rows),
            '变更等级': np.random.choice(['一级', '二级', '三级'], n_rows, p=[0.2, 0.3, 0.5]),
            '影响产品安全特性': np.random.choice(['是', '否', None], n_rows, p=[0.1, 0.8, 0.1]),
            '影响客户装配界面': np.random.choice(['是', '否', None], n_rows, p=[0.15, 0.75, 0.1]),
            '影响 CATL 装配界面': np.random.choice(['是', '否', None], n_rows, p=[0.2, 0.7, 0.1]),
            '当前节点': np.random.choice(['主导人审核', 'CFT1 评审', 'CFT2 评审', '断点确认', '已关闭'], n_rows),
            '流程状态': np.random.choice(['未归档', '已归档', '进行中'], n_rows, p=[0.4, 0.4, 0.2]),
            '主导人': np.random.choice(['赵奇绘', '林宋锦', '王文杰', '昊淮钰'], n_rows),
            '审核完成日期': pd.date_range('2026-01-02', periods=n_rows, freq='H'),
            'CFT1 线下会议完成日期': pd.date_range('2026-01-03', periods=n_rows, freq='H'),
            'CFT1 变更评审完成日期': pd.date_range('2026-01-04', periods=n_rows, freq='H'),
            'CFT2 线下会议完成日期': pd.date_range('2026-01-05', periods=n_rows, freq='H'),
            'CFT2 变更评审完成日期': pd.date_range('2026-01-06', periods=n_rows, freq='H'),
            '主导人断点确认日期': pd.date_range('2026-01-07', periods=n_rows, freq='H'),
            '主导人部门': np.random.choice(['工程部', '质量部', '采购部', '研发部'], n_rows),
        })
        df = df_sample
        st.success("已加载示例数据（1000 条）")
else:
    st.success(f"✅ 已加载数据 {len(df)} 条")

# ==================== 侧边栏筛选器 ====================
st.sidebar.header("🔍 筛选条件")
st.sidebar.markdown("---")

# 日期筛选
if '申请日期' in df.columns:
    df['申请日期'] = pd.to_datetime(df['申请日期'])
    min_date = df['申请日期'].min().date()
    max_date = df['申请日期'].max().date()

    date_range = st.sidebar.date_input(
        "📅 申请日期范围",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        df = df[(df['申请日期'] >= pd.Timestamp(date_range[0])) & (df['申请日期'] <= pd.Timestamp(date_range[1]))]

# 变更项目筛选
if '一级变更项目' in df.columns:
    project_types = st.sidebar.multiselect(
        "📋 变更项目类型",
        options=df['一级变更项目'].dropna().unique(),
        default=df['一级变更项目'].dropna().unique()
    )
    df = df[df['一级变更项目'].isin(project_types)]

# 变更等级筛选
if '变更等级' in df.columns:
    levels = st.sidebar.multiselect(
        "🎯 变更等级",
        options=df['变更等级'].dropna().unique(),
        default=df['变更等级'].dropna().unique()
    )
    df = df[df['变更等级'].isin(levels)]

# 流程状态筛选
if '流程状态' in df.columns:
    status = st.sidebar.multiselect(
        "📍 流程状态",
        options=df['流程状态'].dropna().unique(),
        default=df['流程状态'].dropna().unique()
    )
    df = df[df['流程状态'].isin(status)]

# 主导人筛选
if '主导人' in df.columns:
    owners = st.sidebar.multiselect(
        "👤 主导人",
        options=df['主导人'].dropna().unique(),
        default=df['主导人'].dropna().unique()
    )
    df = df[df['主导人'].isin(owners)]

st.sidebar.markdown("---")
st.sidebar.info(f"📊 当前筛选数据：**{len(df)} 条**")

# ==================== 关键指标卡片 ====================
st.subheader("📈 关键指标 KPI")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("📋 总单量", f"{len(df)}")

with col2:
    if '流程状态' in df.columns:
        ongoing = len(df[df['流程状态'].isin(['未归档', '进行中'])])
        st.metric("🔄 进行中", f"{ongoing}")

with col3:
    if '流程状态' in df.columns:
        completed = len(df[df['流程状态'] == '已归档'])
        st.metric("✅ 已完成", f"{completed}")

with col4:
    if '零件重要等级' in df.columns:
        critical = len(df[df['零件重要等级'] == '关键件'])
        st.metric("⚠️ 关键件", f"{critical}")

with col5:
    if '变更等级' in df.columns:
        level1 = len(df[df['变更等级'] == '一级'])
        st.metric("🔴 一级变更", f"{level1}")

with col6:
    if '变更等级' in df.columns:
        level3 = len(df[df['变更等级'] == '三级'])
        st.metric("🟢 三级变更", f"{level3}")

st.markdown("---")

# ==================== 第一行：趋势 + 类型 ====================
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.subheader("📅 月度变更趋势")
    if '申请日期' in df.columns:
        # 确保日期已转换
        df['申请日期'] = pd.to_datetime(df['申请日期'], errors='coerce')
        # 按月分组统计
        trend_df = df.groupby(pd.Grouper(key='申请日期', freq='M')).size().reset_index(name='单量')
        # 格式化月份显示
        trend_df = trend_df[trend_df['申请日期'].notna()]
        if len(trend_df) > 0:
            trend_df['月份'] = trend_df['申请日期'].dt.strftime('%Y-%m')
            st.bar_chart(trend_df.set_index('月份')['单量'], use_container_width=True)
        else:
            st.write("暂无有效日期数据")

with col2:
    st.subheader("🔄 5M1E 变更类型")
    if '一级变更项目' in df.columns:
        type_dist = df['一级变更项目'].value_counts()
        st.write(type_dist)

with col3:
    st.subheader("🎯 变更等级分布")
    if '变更等级' in df.columns:
        level_dist = df['变更等级'].value_counts()
        st.write(level_dist)

# ==================== 第二行：零件等级 + 物料类型 ====================
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📦 零件重要等级")
    if '零件重要等级' in df.columns:
        part_dist = df['零件重要等级'].value_counts()
        st.write(part_dist)

with col2:
    st.subheader("🏭 物料类型 TOP10")
    if '物料类型' in df.columns:
        material_dist = df['物料类型'].value_counts().head(10)
        st.bar_chart(material_dist, use_container_width=True)

with col3:
    st.subheader("🏢 主导人部门分布")
    if '主导人部门' in df.columns:
        dept_dist = df['主导人部门'].value_counts()
        st.write(dept_dist)

st.markdown("---")

# ==================== 第三行：人员分析 ====================
st.subheader("👥 人员工作量分析")

col1, col2 = st.columns(2)

with col1:
    st.subheader("主导人工作量 TOP10")
    if '主导人' in df.columns:
        owner_dist = df['主导人'].value_counts().head(10)
        st.bar_chart(owner_dist, use_container_width=True)

with col2:
    st.subheader("工程师协同分析")
    engineer_cols = ['CATL 设计工程师', 'CATL 部 PMC-MC 工程师', 'CATL SQE 工程师', 'CATL SRC 工程师']
    engineer_data = {}
    for col in engineer_cols:
        if col in df.columns:
            engineer_data[col.replace('CATL', '').strip()] = df[col].value_counts().sum()

    if engineer_data:
        st.write(pd.DataFrame(engineer_data.items(), columns=['角色', '参与次数']))

# ==================== 第四行：供应商 + 原因 ====================
st.subheader("🏪 供应商与变更原因分析")

col1, col2 = st.columns(2)

with col1:
    st.subheader("供应商 TOP10")
    if '供应商代码' in df.columns:
        supplier_dist = df['供应商代码'].value_counts().head(10)
        st.bar_chart(supplier_dist, use_container_width=True)

with col2:
    st.subheader("变更触发原因")
    if '变更触发原因分类' in df.columns:
        reason_dist = df['变更触发原因分类'].value_counts()
        st.write(reason_dist)

# ==================== 第五行：影响评估 ====================
st.subheader("⚠️ 影响评估分析")

col1, col2, col3 = st.columns(3)

with col1:
    if '影响产品安全特性' in df.columns:
        safety_dist = df['影响产品安全特性'].fillna('未评估').value_counts()
        st.write("**影响产品安全特性**")
        st.write(safety_dist)

with col2:
    if '影响客户装配界面' in df.columns:
        customer_dist = df['影响客户装配界面'].fillna('未评估').value_counts()
        st.write("**影响客户装配界面**")
        st.write(customer_dist)

with col3:
    if '影响 CATL 装配界面' in df.columns:
        catl_dist = df['影响 CATL 装配界面'].fillna('未评估').value_counts()
        st.write("**影响 CATL 装配界面**")
        st.write(catl_dist)

st.markdown("---")

# ==================== 第六行：流程节点 ====================
st.subheader("📍 流程节点分布")

if '当前节点' in df.columns:
    node_data = df['当前节点'].value_counts()

    # 用进度条展示
    total = node_data.sum()
    for node, count in node_data.items():
        pct = (count / total) * 100
        st.write(f"**{node}**: {count} ({pct:.1f}%)")
        st.progress(int(pct) if pct <= 100 else 100)

st.markdown("---")

# ==================== 第七行：交叉分析 ====================
st.subheader("🔀 交叉分析")

col1, col2 = st.columns(2)

with col1:
    st.subheader("变更类型 × 变更等级")
    if '一级变更项目' in df.columns and '变更等级' in df.columns:
        cross_tab = pd.crosstab(df['一级变更项目'], df['变更等级'])
        st.write(cross_tab)

with col2:
    st.subheader("零件等级 × 变更等级")
    if '零件重要等级' in df.columns and '变更等级' in df.columns:
        cross_tab2 = pd.crosstab(df['零件重要等级'], df['变更等级'])
        st.write(cross_tab2)

# ==================== 原始数据查看 ====================
st.markdown("---")
st.subheader("📄 原始数据明细")

with st.expander("查看/导出原始数据"):
    st.dataframe(df, use_container_width=True)

    # 提供下载按钮
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 下载当前筛选数据为 CSV",
        data=csv,
        file_name=f"scm_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# ==================== 页脚 ====================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
        🏠 本地部署 - 数据完全保存在公司内网 |
        最后更新：""" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
    </div>
    """,
    unsafe_allow_html=True
)
