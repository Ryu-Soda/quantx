import numpy as np
import pandas as pd
import talib as ta

def initialize(ctx):
    # 設定
    ctx.logger.debug("initialize() called")
    ctx.configure(
      channels={          # 利用チャンネル
        "jp.stock": {
          "symbols": [
            "jp.stock.2768",
            "jp.stock.8001",
            "jp.stock.8002",
            "jp.stock.8015",
            "jp.stock.8031",
            "jp.stock.8053",
          ],
          "columns": [
            "per",                # PER
            "pbr",                # PBR
            "eps",                # EPS
            "net_sales",          #売上
            "divident_payout"     #配当性向
            ]
          }
      }
    )

    def _my_signal(data): #シグナル作成に必要なデータを作成する
      #使いたいデータのデータフレームを作成
      #cp = data["close_price_adj"].fillna(method="ffill")     #終値
      #EPS = data["eps"].fillna(method="ffill")
      #per0 = data["per"].fillna(method="ffill")                 #[]内と同じ名前を付けるとエラーが出る
      #dp = data["divident_payout"].fillna(method="ffill")       #配当性向
      #div = pd.DataFrame(data=0,columns=[], index=cp.index)     #配当金
      #divp = pd.DataFrame(data=0,columns=[], index=cp.index)    #配当利回り
      #divp5 = pd.DataFrame(data=0,columns=[], index=cp.index)   #配当利回りの五日平均
      #divp5p = pd.DataFrame(data=0,columns=[], index=cp.index)  #一日前の配当利回りの五日平均
      #PER = pd.DataFrame(data=0,columns=[], index=cp.index)
 
      #PER = 株価÷一株当たり純利益
      #配当利回り＝配当性向＊一株当たり純利益÷株価

      #for(sym,val) in cp.items():
        #PER[sym] = cp[sym]/EPS[sym]
        #div[sym] = EPS[sym]*dp[sym]
        #divp[sym] = div[sym]/cp[sym]
        #divp5[sym] = ta.SMA(divp[sym].values.astype(np.double) , timeperiod=5)
        #divp5p[sym] = divp5[sym].shift()
      return {
        #"per0":per0,
        #"EPS":EPS,
        #"PER":PER,
        #"div":div,
        #"divp":divp,
        #"divp5":divp5,
        #"divp5p":divp5p,
        #"dp":dp,
        
      }

    # シグナル登録
    ctx.regist_signal("my_signal", _my_signal)

def handle_signals(ctx, date, current): #シグナルを作成する
    '''
    current: pd.DataFrame
    
    
    '''
    #done_syms = set([])
    #divp5 = current["divp5"].dropna()
    #divp5p = current["divp5p"].dropna()
    
    #buy_sig = divp5[(divp5>4.5) & (divp5p<4.5)] #
    #sell_sig = divp5[divp5<3]
    
    #for (sym,val) in buy_sig.items():
      #sec = ctx.getSecurity(sym)
      #sec.order(sec.unit() * 1, comment="SIGNAL BUY")
  
    #for (sym,val) in sell_sig.items():
      #sec = ctx.getSecurity(sym)
      #sec.order_target_percent(0, comment="SIGNAL SELL")

    #done_syms = set([])
    #for (sym,val) in ctx.portfolio.positions.items():
    #    returns = val["returns"]
    #    if returns < -0.03:
    #      sec = ctx.getSecurity(sym)
    #      sec.order(-val["amount"], comment="損切り: %f" % returns)
    #      done_syms.add(sym)
    #    elif returns > 0.05:
    #      sec = ctx.getSecurity(sym)
    #      sec.order(-val["amount"], comment="損益確定売: %f" % returns)
    #      done_syms.add(sym)

    #buy = current["buy:sig"].dropna()
    #buy = buy[~buy.index.isin(done_syms)]
    #for (sym,val) in buy.items():
    #    sec = ctx.getSecurity(sym)
    #    sec.order(sec.unit() * 1, comment="SIGNAL BUY")
    #    done_syms.add(sym)
    #    ctx.logger.debug("BUY: %s,  %f" % (sec.code(), val))
    #
    #sell = current["sell:sig"].dropna()
    #sell = sell[~sell.index.isin(done_syms)]
    #for (sym,val) in sell.items():
    #    sec = ctx.getSecurity(sym)
    #    sec.order(sec.unit() * -1, comment="SIGNAL SELL")
    #    done_syms.add(sym)
    #    ctx.logger.debug("SELL: %s,  %f" % (sec.code(), val))
