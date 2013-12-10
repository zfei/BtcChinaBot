BTC China Bot
===========

This bot runs on [BTC China](https://vip.btcchina.com), aka the heaven of trading bots, where transaction fee is 0%.
Currently it only follows simple heuristics (buy low and sell high). The assumption for this to work is that the market price is constantly changing, you can also buy at highest bid price and sell a little lower than lowest ask price.

I decided to open source the trading bot, hoping people can benefit from or, even better, contribute to the project and make it better.

Usage
---

``` bash
git clone https://github.com/zfei/BtcChinaBot
```
after it's downloaded, cd into BtcChinaBot:
``` bash
cd ./BtcChinaBot
```
rename sample_settings.py to settings.py:
``` bash
mv sample_settings.py settings.py
```
and make changes to it (set API key & secret and parameters).

Finally, run the bot:
``` bash
python bot.py
```
This program is provided AS IS. Use it at your own risk.

License
---

The use of this program is subject to MIT LICENSE, please read LICENSE in the project folder if you do not know about it.


---



I've made more than 5 changes to it to actually make it work.

I've also spent much time (several nights right before a final exam) to tune the program so that it behaves.



``` bash
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```


