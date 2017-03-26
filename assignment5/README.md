
README
---
### Task 1

Below is something I found tricky and solved:
- If you set the date first,  input the from & to city will automatically reset to the default date. **So set date after input**.
- We need to **wait** for the website to load data. 

### Task 2

I solved problem like:
- When click to see the rest 30 days, the displayed **order of cities will change**. 
- Somehow you **cannot click the page-down arrow** of the city when your mouse hover over the last bar, we need to click that arrow of another city.
- **TIME DIFFRENCE!** when you use 'TODAY' as start date and meanwhile, your start city is london/china etc., you will have a time difference issue. See my code for solution.

### Task 3

**Part 1:**
I used grid search and subplots to find decent hyper parameters. The script is in the same folder.

**Part 2:**
This method performs bad. Almost can't find good price.

**Part 3:**

[**Novelty and Outlier Detection**](http://scikit-learn.org/stable/modules/outlier_detection.html)

The following is my concerns of which algorithm to chose:
- Based on observing, the date we have is not unimodal, there should be mulitple cluster in one graph. Robust covariance seem to work well in unimodal.
- Isolation Forest works in high dimension, which is not in this case.
- 'One-class SVM gives useful results when we don't have assumptions on the distribution' Maybe we should use this!
**So I chose One-class SVM**. But, just some naive thoughts, tell me if I was wrong.
By choosing 2 typical case and subploting different parameter combinations I will take para '''kernel = sigmoid, nu =0.1''' and set others as default

### Task 4

For better performance we need to scale the X dimension so that DBSCAN will generate priod of continuous days based on formula: $\sqrt{ x ^2 + 20 ^2 } <  2x $ ,$x \gt \sqrt{ \frac{20^2}{3}}$ and then set a littler bigger x.

