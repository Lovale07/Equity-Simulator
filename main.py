import random
import numpy as np
# import time
import matplotlib.pyplot as plt

# startTime = time.time()

averageRRR = 10  # between 0 and 1000 included, float
winrate = 20  # between 0 and 100 excluded, float
numberOfTradesPerMonth = 15  # between 1 and 1000 included, integer
startingCapital = 10000  # between 1 and 1,000,000,000 included, integer
numberOfMonthsToIterate = 12  # between 1 and 1200 included, integer
maxDrawdownWanted = 10  # between 0 and 100% excluded, float
numberOfTradesToDetermineRisk = 10000
numberOfIterationsToDetermineRisk = 100


# First iteration to determine how much to risk relative to the max drawdown
maxDrawdownEncountered = 0

for n in range(numberOfIterationsToDetermineRisk):

    trade_returns = np.zeros(numberOfTradesToDetermineRisk)
    balances = np.zeros(numberOfTradesToDetermineRisk)
    drawdowns = np.zeros(numberOfTradesToDetermineRisk)
    max_drawdowns = np.zeros(numberOfTradesToDetermineRisk)

    drawdownStart = startingCapital
    inDrawdown = False
    drawdown = 0
    maxDrawdown = 0

    tradeReturn = averageRRR if random.randrange(100) < winrate else -1
    new_balance = startingCapital * (1 + tradeReturn * 0.01)
    if new_balance < startingCapital:
        drawdown = (drawdownStart - new_balance) / drawdownStart
        inDrawdown = True

    trade_returns[0] = tradeReturn
    balances[0] = new_balance
    drawdowns[0] = drawdown
    max_drawdowns[0] = drawdown

    for index in range(1,numberOfTradesToDetermineRisk):

        tradeReturn = averageRRR if random.randrange(100) < winrate else -1
        new_balance = balances[index-1] * (1 + tradeReturn * 0.01)
        if inDrawdown:
            if new_balance < drawdownStart:
                drawdown = (drawdownStart - new_balance) / drawdownStart
                maxDrawdown = max(drawdown,maxDrawdown)
            else:
                inDrawdown = False
                drawdown = 0
        elif new_balance < balances[index-1]:
            inDrawdown = True
            drawdownStart = balances[index-1]
            drawdown = (drawdownStart - new_balance) / drawdownStart
            maxDrawdown = max(drawdown,maxDrawdown)

        trade_returns[index] = tradeReturn
        balances[index] = new_balance
        drawdowns[index] = drawdown
        max_drawdowns[index] = maxDrawdown

    # print(f"Max drawdown from the iteration {n+1} : {maxDrawdown}")

    maxDrawdownEncountered = max(maxDrawdown,maxDrawdownEncountered)

risk = ((maxDrawdownWanted)/ (maxDrawdownEncountered * 100))/100
# print(f"Max drawdown from all the iterations : {maxDrawdownEncountered}")
# print(f"Risk recommended : {round(risk*100, 2)}%")

# Last iteration in which we simulate the equity growth with the new found recommended risk

trade_returns = np.zeros(numberOfMonthsToIterate*numberOfTradesPerMonth)
balances = np.zeros(numberOfMonthsToIterate*numberOfTradesPerMonth)
drawdowns = np.zeros(numberOfMonthsToIterate*numberOfTradesPerMonth)
max_drawdowns = np.zeros(numberOfMonthsToIterate*numberOfTradesPerMonth)

drawdownStart = startingCapital
inDrawdown = False
drawdown = 0
maxDrawdown = 0

tradeReturn = averageRRR if random.randrange(100) < winrate else -1
new_balance = startingCapital * (1 + tradeReturn * 0.01)

balances[0] = new_balance

for index in range(1, numberOfMonthsToIterate*numberOfTradesPerMonth):

    tradeReturn = averageRRR if random.randrange(100) < winrate else -1
    new_balance = balances[index-1] * (1 + tradeReturn * 0.01)

    balances[index] = new_balance

#plot (we can also transform the array into a pandas dataframe then plot)
x = np.zeros(numberOfMonthsToIterate*numberOfTradesPerMonth)
for index in range(1,numberOfMonthsToIterate*numberOfTradesPerMonth):
    x[index] = index

color = "green" if balances[(numberOfMonthsToIterate*numberOfTradesPerMonth)-1] > balances[0] else "red"

plt.title(f"Balance (recommended risk : {round(risk*100, 2)}%)")
plt.xlabel("Number of trades")
plt.ylabel("Dollars")
plt.plot(x, balances, color = color)

# elapsed_time = time.time() - startTime
# print(f"Time taken : {elapsed_time//60}min {elapsed_time%60}s")

plt.show()
