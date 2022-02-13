# algotrading
An algo strategy that actually works and has also been backtested.

Background: I have been following the Indian equity market for the past 3 years and have been actively following the stock market since March,2020. One day around this time, I came across a new fund offered by True Beacon, a new asset management company co-founded by Mr.Nikhil Kamath(Co-founder of Zerodha). They were offering an AIF(Alternate Investment Fund) that would invest 60% in equity and the rest of the capital is deployed in derivatives to hedge their long only positions. The proposed alpha of this fund over NIFTY-50 is around 6 percent (i.e., it would give 16% return if NIFTY gives 10% CAGR). This product intrigued me and I started researching much into the subject. The question I had in my mind is, how can anyone generate higher return while making the fund less volatile. After some research and self-learning, I realized that one can do trading following a mathematical model/strategy and earn money (unlike the popular notion of losing money by trading). Being a data scientist myself, I wanted to explore more into this subject and this blog is the result of one such strategy that I explored in the process. Personally, I don’t believe in popular strategies like mean reversion, bollinger bands etc. I wanted to build a strategy in which I can define the logic and control the risk rate.

In this blog, I want to talk about a strategy that has given me blockbuster returns. The goal of this blog is not to encourage people to start trading but to defy the popular notion that trading in the stock market is similar to gambling/speculative bets.

Note: I consider myself a novice and a risk averse investor in the equity market. I still invest 50% of my investments through SIP in mutual funds. (Rather than investing directly in the stocks).

The strategy:
1)	Shortlist a stock of your interest
2)	Predict the high and low price of the company’s share price next day based on the previous day's close price.
3)	Place orders based on the predicted high and low price.
4)	Our profit will be the margin we would make in these two trades (Typically, 1% to 2%)

We will evaluate the model based on the returns we could generate using this strategy and the success rate of trades every trading day.

Evaluation metrics: Success Rate and Returns of the share

Success Rate: Trades executed on a respective date is considered a success if the profit margin crosses 0.20%.

Returns: Returns mentioned in this blog are not annualized. Annualized return would be much higher than the mentioned returns in this blog. 

Returns observed in the year 2021

![image](https://user-images.githubusercontent.com/49510297/153766493-17fa7d40-224f-460e-9cbf-2060f22e9d23.png)

Returns observed between 2015-2021

![image](https://user-images.githubusercontent.com/49510297/153766511-b458ca85-e779-471a-b52b-16df51d1c1b4.png)


Refer to this blog for more details:

