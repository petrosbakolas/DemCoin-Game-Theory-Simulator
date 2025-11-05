# How to Use the Simulator

## For Non-Programmers (Petros, this is for you! 😄)

You don't need to understand Python. Just:

1. Go to https://replit.com or https://colab.research.google.com
2. Upload the `simulator.py` file
3. Click "Run"
4. See the predictions!

## What the Output Means
```
Participation Rate: 42.3%
```
→ With current parameters, 42% of citizens will engage
```
Average Quality: 7.8/10
```
→ Those who participate will contribute high-quality analysis
```
Optimal DemCoin per hour: 20
```
→ To get 50%+ participation, increase rewards to 20 DemCoins/hour

## Changing Parameters

In the code, find this section:
```python
sim = DemCoinSimulator(
    num_citizens=1000,
    demcoin_per_hour=15,  # ← Change this number
    success_bonus=100,     # ← Change this number
    time_cost=3            # ← Change this number
)
```

**Try:**
- Increase `demcoin_per_hour` to 25 → See participation increase
- Increase `success_bonus` to 200 → See long-term thinkers increase
- Decrease `time_cost` to 1 → See what happens if decisions are simpler

## Understanding Game Theory Predictions

The simulator finds the **Nash Equilibrium** - the stable point where nobody wants to change their decision.

If it says "Participation: 45%", that means:
- 45% will study because it's worth it for them
- 55% will ignore because it's not worth their time
- Nobody in either group wants to switch

**This is the PREDICTION of how real people will behave.**

## Next Steps

Once you see predictions you like:
1. Note the parameters that work
2. Use those in the actual DemCoin smart contract
3. Launch pilot
4. Measure real results
5. Compare to predictions
6. Adjust!
