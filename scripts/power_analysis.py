#A priori power analysis to determine experiment requirements for accuracy
#will figure out how many participants need to be given the forms

#import
from statsmodels.stats.power import TTestPower

analysis = TTestPower()

#Assumptions being used
# paired t test with the same group doing AI and non AI trivia - experiment design
# Group 1 will complete Quiz A with AI and Quiz B with no AI and Group 2 will complete quiz A with no AI and quiz B with AI
# Using Cohen's size benchmarks for behavior experiments, we are shooring for a medium effect of d=0.5
# Alpha 0.05 with standard cutoff of 5% false positive
# Power at .80 also driven by cohen standards

needed = analysis.solve_power(effect_size=0.5, alpha=0.05, power=0.8)
print(f"The estimated participants needed for medium effect 80% power is: {needed:.0f}")
print("Note: If number ends up being smaller than goal, mention it in  limitations.")

