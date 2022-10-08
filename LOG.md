### 7/10/22 (night time)

- Notes:
  - From looking at the plots, we will definitely need to smooth out the 
    data. There are moments when the values will drop precipitously. 
    - [] Clean/ smooth out the data. Get rid of the precipitous drops. 
  - **A big thing to note is that the sector timings are very different in 
  this dataset compared to the live timings on the superTaikyu website (I'm
  guessing those are for a different race.**
    - The sector timings are: 25.6, 25.8, 36.3, 17.3


### 2/10/22

Working notes:

- We now have the indices where the laps change values... therefore we can get all of the values for a given Lap
  - Coming back, we will want to use use Lap Dist covered in order to get the sectors... but for now we will just use
  whole laps
- Let's fill all the values between two row indicies into some lists. We can then plot them... we can probs even just
  use pandas.Series
- **Actually I'm not thinking super clearly right now (too late + loud in here) so I am just going to make this work with lists or numpy arrays**
     ** + matplotlib, and then we can come back and make it work with pandas.Series**


