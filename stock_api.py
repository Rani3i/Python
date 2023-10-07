import baostock as bs
import pandas as pd
import mysql.connector
import datetime

# 登陆系统
bs.login()

# 连接MySQL数据库
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='stock'
)

# 从MySQL数据库中获取股票代码和名称
cursor = conn.cursor()
cursor.execute("SELECT code, name FROM stock_codes")
stock_codes = {code: name for code, name in cursor.fetchall()}


# 获取今天的日期并自己设置结束日期 （也能自己设置开始时间）
today = datetime.date.today()
end_date = "2022-01-01"

# 遍历股票代码和名称
for stock_code, stock_name in stock_codes.items():
    # 查询数据
    rs = bs.query_history_k_data_plus(stock_code,
                                      "date,open,high,low,close,volume",
                                      start_date=end_date,
                                      end_date=today.strftime("%Y-%m-%d"),
                                      frequency="d",
                                      adjustflag="3")
    # 将数据存储在DataFrame中
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result['code'] = stock_code
    result['name'] = stock_name
    result['close'] = result['close'].astype(float) # 将close列转换为float类型
    result['pct_change'] = result['close'].pct_change() * 100
    result['up_down'] = result['pct_change'].apply(lambda x: 'up' if x > 0 else 'down')
    result.dropna(subset=['pct_change'], inplace=True)

    # 将数据存储到MySQL数据库中
    cursor = conn.cursor()
    table_name = 'stock_data'
    columns = ', '.join(result.columns)
    values = ', '.join(['%s' for _ in range(len(result.columns))])
    for row in result.itertuples(index=False):
        insert_sql = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({values})"
        cursor.execute(insert_sql, row)
    conn.commit()

    # 打印完成获取的股票代码和名称
    print(f"完成获取股票代码：{stock_code} 股票名称：{stock_name} 从 {end_date} 到 {today}")

# 关闭连接
conn.close()

# 登出系统
bs.logout()
