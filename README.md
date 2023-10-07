index_api (Baostock)
- 可以获得到5个主要的中国指数信息；
- 可自行设置时间；
- 其中增加了和MySQL的连接部分，可自行更改host,user,password,database。
- 获取数据为 （date,open,high,low,close,volume）

stock_api (Baostock)
- 可根据MySQL中存储的股票代码来进行特定的股票数据获取；
- 其中增加了和MySQL的连接部分，可自行更改host,user,password,database；
- 可自行设置时间；
- 获取数据为 （date,open,high,low,close,volume）。

industry_api (AKShare)
- 这个API接口需要提前将行业中所有的股票代码输入进去MySQL，输入后可根据指定的股票代码获取数据；
- 由于Baostock没有北交所的股票数据，因此选择数据更加完整的AKShare来作为补充；
- 可自行设置时间；
- 获取数据为 (industry, stock_code, date, open, high, low, close, volume, outstanding_share, turnover, pct_change)
