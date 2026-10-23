# Hypothesis: total is never reset for each person, so it keeps adding up.
# Also ">" should be ">=" so exactly 10,000 gets Gold.
weekly_steps = {
   "Kai":     [8000, 9500, 7200, 11000, 6800, 12000, 9000],
   "Leilani": [12000, 9000, 10500, 8500, 11000, 9500, 9500],
   "Noa":     [4000, 5200, 3800, 6100, 4500, 5000, 4400],
}
def choose_badge(average):
   if average >= 10000:
       return "Gold"
   elif average >= 7500:
       return "Silver"
   else:
       return "Bronze"
 
for name in weekly_steps:
   total = 0
   days = weekly_steps[name]
   for steps in days:
       total += steps
   average = total / len(days)
   badge = choose_badge(average)
   print(name.ljust(8), "average:", format(average, ",.0f"), "steps/day ->", badge)
 
# Edge case tests
print(choose_badge(10000), choose_badge(7500), choose_badge(7499))
