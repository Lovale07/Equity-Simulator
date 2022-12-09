This program shows the balance growth of any given strategy depending on the following parameters :
- winrate
- averageRRR (average return per trade)

You can choose to run the strategy over how much time you want, with the starting capital you want, just modify :
- startingCapital
- numberOfTradesPerMonth
- numberOfMonthsToIterate

Since every result is proportional to the risk we take, we need to have a similar maximum drawdown in order to compare the strategies. Modify maxDrawdownWanted
depending on your risk appetite. 

The program runs a number of trades to determine the maximum drawdown of the strategy. This number depends on numberOfTradesToDetermineRisk and 
numberOfIterationsToDetermineRisk. The maximum drawdown found is then used to calculate a recommended risk : if we risk that amount per trade, we have a high chance
of never reaching the maximum dradown wanted. So the higher these two variables are, the less chance we have of hitting maxDrawdownWanted. The balance on the graph is 
adjusted depending on this risk as well.

