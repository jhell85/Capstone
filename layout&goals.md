# Skinonit Website
create a web application that lets users create a profile and place bets with other users on stuff from sports, tv show outcomes, award show results, death pools or any other type of wager. also include a regular text written bet option that can't be defined who was the winner of the bet except for the users involved in the bet. the site will not facilitate the exchange of money but will allow users to pay their bets using Venmo, Cash app or PayPal with links to the appropiate sites. the site will have a rating for system for users to rate other users based on bets that were placed between each other. The rating system will allow for users to know if the person they are betting with is legit to pay up if they loose and would also allow to place the user who didn't pay on the Wall of Shame a place to shame people who don't pay their bets.
## Home page
1. Create bet
2. User profile home page
3. Check open bets made by other users
4. Check open bets that user has created
    - bets that have been accepted by another user
    - bets that are still waiting to be accepted by another user
5. Check completed bets that have and haven't been paid out
6. Wall of Shame
## Data Model
1. Users
    - Name
    - email 
    - rating (5 star rating system )
    - profile picture
    - bio 
    - Open bets the user is involved in
        - Bets that have been accepted by another user
        - Bets that are still waiting to be accepted by another user (open bet)
    - Closed bets the user is involved in
        - Bets that have been agreed by all users involved that the outcome was settled 
        - Bets that have not been agreed to being settled 
2. Bets
    - odds placed bets 
        - give users the options to change odds but show what vegas or other online casinos are offering in odds play
    - give users options to bet with points giving or reciving points to a certian side
    - straight up bet no odds
    - text base bets

        
