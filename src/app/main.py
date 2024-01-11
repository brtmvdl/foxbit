from datetime import datetime
import flet
import config
import threading
import foxbit
import datetime

# models

class PairModel():
  def __init__(self, base: str, quote: str):
    self._base = base
    self._quote = quote

  def __str__(self) -> str:
    return (self._base + self._quote).upper()

# components

Separator = lambda: flet.Divider(color = config.color)

class CoinComponent(flet.Tab):
  def __init__(self, pair: PairModel("", ""), on_update = lambda: print("update")):
    super().__init__()
    self.on_update = on_update
    self.pair = pair
    self.text = str(pair)
    self.__datetime = flet.Text("now")
    self.__price = flet.Text("0.0")
    self.__amount = flet.TextField(label = "Amount", input_filter = flet.NumbersOnlyInputFilter())
    self.__buy = flet.TextButton("Buy", on_click=self.on_buy_click)

    self.__buys = flet.Row([])
    top = flet.Row([flet.Text("datetime: "), self.__datetime,  flet.Text("price: "), self.__price, self.__amount, self.__buy,])

    self.content = flet.Column([Separator(), top, Separator(), self.__buys])
    self.set_interval(self.update_text, 1.25)

  def createKeyValuePair(self, key, value):
    return flet.Column([
      flet.Text(str(key)), 
      flet.Text(str(value)),
    ])

  def on_buy_click(self, e):
    t = threading.Thread(target = self.buy, args = ())
    t.start()

  def buy(self):
    sell = flet.Column()

    def on_sell():
      sell.controls.append(self.createKeyValuePair("datetime: ", ""))
      sell.controls.append(self.createKeyValuePair("price: ", ""))
      sell.controls.append(self.createKeyValuePair("gain: ", ""))

    buy = flet.Column()
    buy.controls.append(self.createKeyValuePair("datetime: ", ""))
    buy.controls.append(self.createKeyValuePair("price: ", ""))
    buy.controls.append(self.createKeyValuePair("amount: ", ""))

    self.__buys.controls.append(buy)
    self.__buys.controls.append(sell)
    self.__buys.controls.append(flet.TextButton("Sell", on_sell))

    self.on_update()

  def update_text(self):
    self.__datetime.value = str(datetime.datetime.now())
    res = foxbit.GetMarketQuotation("buy", self.pair._base, self.pair._quote, "100.00")
    self.__price.value = str(res.getPrice())
    self.on_update()

  def set_interval(self, func, sec: float = 1):
    def func_wrapper():
      func()
      self.set_interval(func, sec)
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

# main

def main(page: flet.Page):
  page.title = config.app_name
  page.add(flet.Tabs(tabs = [
    CoinComponent(PairModel("btc", "brl"), lambda: page.update()),
    CoinComponent(PairModel("eth", "brl"), lambda: page.update()),
    CoinComponent(PairModel("ltc", "brl"), lambda: page.update()),
  ]))

if __name__ == "__main__":
  flet.app(target = main)
