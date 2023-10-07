import mysql.connector
import akshare as ak

# 连接MySQL数据库
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='stock'
)

# 从数据库中获取行业和股票代码
cursor = conn.cursor()
cursor.execute("SELECT industry, stock_code FROM industry_code")
industry_codes = cursor.fetchall()

# 获取开始日期和结束日期
start_date = "2022-04-29"
end_date = "2023-04-29"

# 创建一个空的列表用于存储数据
data_list = []

# 遍历行业和股票代码
for industry, stock_code in industry_codes:
    # 查询数据
    stock_data = ak.stock_zh_a_daily(symbol=stock_code, start_date=start_date, end_date=end_date)
    if stock_data is not None:
        stock_data['industry'] = industry
        stock_data['stock_code'] = stock_code
        stock_data['close'] = stock_data['close'].astype(float)
        stock_data['pct_change'] = stock_data['close'].pct_change() * 100

        # 调整列的顺序
        stock_data = stock_data[['industry', 'stock_code', 'date', 'open', 'high', 'low', 'close', 'volume', 'outstanding_share', 'turnover', 'pct_change']]

        # 删除包含NaN值的行
        stock_data = stock_data.dropna()

        # 将数据添加到data_list列表中
        data_list.append(stock_data)

        # 打印完成获取的行业和股票代码
        print(f"完成获取行业：{industry} 股票代码：{stock_code} 从 {start_date} 到 {end_date}")
        # print(stock_data)  # 打印获取到的数据
    else:
        print(f"获取行业：{industry} 股票代码：{stock_code} 失败")

# 将data_list中的数据存储到MySQL数据库中
cursor = conn.cursor()
table_name = 'industry_data'

for df in data_list:
    for row in df.itertuples(index=False):
        # 构造参数化插入语句
        insert_sql = f"INSERT INTO {table_name} (industry, stock_code, date, open, high, low, close, volume, outstanding_share, turnover, pct_change) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_sql, row)

conn.commit()

# 关闭连接
conn.close()


