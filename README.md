# OkayamaDataset

### Plan - overview 

So we need to basically come up with a baseline for the action of the Okayama
circuit, so we can superimpose the RPM, etc. onto other cars racing on the track,
where we will use their latest sector time, to predict their time in the next 
circuit.

We can visualize this basline like a function/ plot where the x-axis is the 
time/ lap distance travelled per sector, and there are multiple y-axis:

- RPM
- Gear 
- Speed 
- Throttle

And we might add more things to track here. 

On race day in Okayama... we can stretch this plot/ function to match the 
expected time of the cars on race day. 

### Plan - steps (broad)

1. For now, we will focus on making plots just for one car, for one lap. 
1. Then we can look at getting averages. 

**What to produce for step one:**

- Matplotlib plots of the car for each sector, with the RPM, gear, speed, throttle