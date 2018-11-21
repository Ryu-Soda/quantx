import numpy as np
import pandas as pd
import talib as ta

def initialize(ctx):
    # �ݒ�
    ctx.logger.debug("initialize() called")
    ctx.configure(
      channels={          # ���p�`�����l��
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
            "net_sales",          #����
            "divident_payout"     #�z������
            ]
          }
      }
    )

    def _my_signal(data): #�V�O�i���쐬�ɕK�v�ȃf�[�^���쐬����
      #�g�������f�[�^�̃f�[�^�t���[�����쐬
      cp = data["close_price_adj"].fillna(method="ffill")     #�I�l
      EPS = data["eps"].fillna(method="ffill")
      per0 = data["per"].fillna(method="ffill")                 #[]���Ɠ������O��t����ƃG���[���o��
      dp = data["divident_payout"].fillna(method="ffill")       #�z������
      div = pd.DataFrame(data=0,columns=[], index=cp.index)     #�z����
      divp = pd.DataFrame(data=0,columns=[], index=cp.index)    #�z�������
      divp5 = pd.DataFrame(data=0,columns=[], index=cp.index)   #�z�������̌ܓ�����
      divp5p = pd.DataFrame(data=0,columns=[], index=cp.index)  #����O�̔z�������̌ܓ�����
      PER = pd.DataFrame(data=0,columns=[], index=cp.index)
 
        
      #PER = cp / eps�@�@�@#PER = �������ꊔ�����菃���v
      #DIVP = eps * dp /cp  #�z������聁�z���������ꊔ�����菃���v������

      for(sym,val) in cp.items():
        PER[sym] = cp[sym]/EPS[sym]
        div[sym] = EPS[sym]*dp[sym]
        divp[sym] = div[sym]/cp[sym]
        divp5[sym] = ta.SMA(divp[sym].values.astype(np.double) , timeperiod=5)
        divp5p[sym] = divp5[sym].shift()
      return {
        "per0":per0,
        "EPS":EPS,
        "PER":PER,
        "div":div,
        "divp":divp,
        "divp5":divp5,
        "divp5p":divp5p,
        "dp":dp,
        
      }

    # �V�O�i���o�^
    ctx.regist_signal("my_signal", _my_signal)

def handle_signals(ctx, date, current): #�V�O�i�����쐬����
    '''
    current: pd.DataFrame
    
    
    '''
    done_syms = set([])
    divp5 = current["divp5"].dropna()
    divp5p = current["divp5p"].dropna()
    
    buy_sig = divp5[(divp5>4.5) & (divp5p<4.5)] #
    sell_sig = divp5[divp5<3]
    
    for (sym,val) in buy_sig.items():
      sec = ctx.getSecurity(sym)
      sec.order(sec.unit() * 1, comment="SIGNAL BUY")
  
    for (sym,val) in sell_sig.items():
      sec = ctx.getSecurity(sym)
      sec.order_target_percent(0, comment="SIGNAL SELL")

    #done_syms = set([])
    #for (sym,val) in ctx.portfolio.positions.items():
    #    returns = val["returns"]
    #    if returns < -0.03:
    #      sec = ctx.getSecurity(sym)
    #      sec.order(-val["amount"], comment="���؂�: %f" % returns)
    #      done_syms.add(sym)
    #    elif returns > 0.05:
    #      sec = ctx.getSecurity(sym)
    #      sec.order(-val["amount"], comment="���v�m�蔄: %f" % returns)
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
