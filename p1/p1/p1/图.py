import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 数据准备
months = ['1月', '2月', '3月', '4月', '5月', '6月']
sales = [624714.4, 372876.99, 500408.59, 505992.3, 626714.12, 535454]

# 创建图表
plt.figure(figsize=(10, 6), dpi=100)
plt.plot(months, sales, marker='o', linestyle='-', color='#1f77b4', linewidth=2, markersize=8)

# 添加标题和标签
plt.title('2023年上半年度销售额趋势', fontsize=15, pad=20)
plt.xlabel('月份', fontsize=12)
plt.ylabel('销售额 (元)', fontsize=12)

# 格式化Y轴显示（每100,000显示刻度）
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
plt.grid(True, linestyle='--', alpha=0.6)

# 在每个数据点上添加数值标签
for x, y in zip(months, sales):
    plt.text(x, y+10000, f'{y:,.2f}', ha='center', va='bottom', fontsize=9)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()