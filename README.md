# Capstone Project Proposal
Create a web application that lets users sign up to be a user on the site and upon signing up the user will receive X amount of credits (points or bucks the name is arbitrary). After the user has signed up they can use those credits to wager bets with one another or let the user wager bets against the house. These bets will be off of sports games (probably start with college basketball), the odds for the payouts as well as the scores for the games will be brought in through a web API. The user will have the option to have different bet bet parameters such as a single team to win to satisfy a winning bet or having multiple teams need to win to satisfy a winning bet(parlay bet). the winning user will be paid out their credits after all bet parameters have been satisfied.

## Name
The name I want to use comes from when I make bets with friends usually the person is confident about their bet would say to the other "Let's put some skin on it", which meant lets bet some money to see who'll win, so I would like to call my project: **Skin on it**

## Project Over View
1. User interface and database 
   - Credit balance 
   - Bets user is actively involved in
   - History of all bets user has been involved in
2. Bets
 - Parameters of bet
   - single parameter bet to determine winner 
   - multiple parameter bet to determine winner, as the parameters change the odds change to match 
   - pool style bets *ex: more then one user in the bet*
     - bracket pools *ex: NCAA march madness bracket* 
     - other pools *ex: Super Bowl squares pool*
   - unofficial bet that only the users would be able to determine the results of the bet *ex: Josh bets Al that Mathew will wear black tomorrow* in this style bet the user would give the odds parameters and amount of the bet to the server. after those are given the users will have to let the server know who was the winner of the bet and distribute credits to the winner based on this.   
3. Data of scores and odds brought in with API  
   - Update the bets users can bet on based on what games have already been played and removing them or making them no longer able to bet on, adding to the bets users can select based on games that haven't been played yet.
 
## Functionality
From the users view they will log in and see a balance of their credits, a link that will state "active bets" and that will take them to a page that has all the bets that are open that they are involved in, another link that will take them to a page where they can place a bet 

## Data Model
1. Users
   - User's basic info 
   - Balance of the user's credits
   - Open bets the user is involved in
   - Finished bets the user was involved in and the results of the bet
2. Bets
   - Parameters of bet to determine what makes a winning bet
   - Odds of the bet to determine how many credits will be paid out to the winning bet 
   - Amount of credits wagered on the bet with this and the odds will determine how much the winner will receive in credits.

## Schedule
### Time line goals
1. Able to finish by Capstone presentation
   - Users- established with ability to create new users and have a section for all the functions of a user outlined in Data model's section
   - Bets- establish ability to place bets against the house or server and payout bets once the bet parameters have been satisfied
   - Scores- use an API to bring in the scores and results of sport events to determine who will be the winner of a bet
2. Possible to finish by Capstone presentation
   - Odds- give the user ability to bet on sporting events with odds brought in with an API to factor into the pay out as opposed to just 1:1 odds
   - User to User betting- give users the ability to bet amongst each other 
3. Functionality to work on past the capstone presentation 
   - pool style bets
   - abilities to bet on more then just sports outcomes *ex: award show nominations and winners*
kgghgkljhiuygibnj