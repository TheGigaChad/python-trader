# Methodology documentation
This document contains relevant logical and architectural decisions regarding the functionality of the algorithmic 
trader.  Although not incredibly in-depth, it will provide a means to understand how it functionally works.     

## Blurb
The trader has two main managers, the Exchange Manager and the Trade Manager.  The logical split was made so that we can
continue doing analysis and data mining and not be concerned about clerical and admin work (previous or current order 
placements within relevant  exchanges and the requirement to log all trades in databases etc.)

## Trade Manager
The Trade Manager (TM) is concerned with evaluating potential or owned assets against pre-designed Neural Networks that
have been created by the Machine Learning Manager (MLM).  If no relevant model exists, it will queue for one to be
created for it and use traditional evaluation metrics to consider the potential for it to be profitable.  

### Operational flow
The operational flow is very simple and operates as a simple Finite State Machine as detailed below.
#### Stopped
The Trade Manager is not running and will not be able to communicate.  This is the 'OFF' state.
#### Initialising 
This is where we initialise the class and determine initial values.
#### Ready  
We are waiting for the Exchange Manager to be running.
#### Running 
Booyah! We are doing our thing until we either error, or kill the application.
#### Stopping 
Process of shutting down.
#### Error 
Houston, we have a problem.

### Components
- Exchange Manager Status
- Trade Instances
- 


### Communication Methodology
The Trade Manager is required to be able to communicate with the Exchange Manager for the following situations:
1. Buy-Sell Threshold Request - Since we have bound the task of all SQL interactions to the Exchange Manager, we send a request to the Exchange Manager asking for the buy and sell thresholds relating to our relevant asset.  This will give us our bounds in which to evaluate or calculated confidence against.
2. 




## Exchange Manager


### Operational flow

### Components
- SQL Manager 
- Exchanges
- Status
- Trade Manager Status
- Order Queue




### Communication Methodology

