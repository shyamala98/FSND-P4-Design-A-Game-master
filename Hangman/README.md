#Full Stack Nanodegree Project 6 - Hangman

## Set-Up Instructions:
1.  Update the value of application in app.yaml to the app ID you have registered
 in the App Engine admin console and would like to use to host your instance of this sample.
1.  Run the app with the devserver using dev_appserver.py DIR, and ensure it's
 running by visiting the API Explorer - by default localhost:8080/_ah/api/explorer.
1.  (Optional) Generate your client library(ies) with the endpoints tool.
 Deploy your application.
 
 
 
##Game Description:
hangman is a word guessing game. Each game begins with a random 'target'
word, and a maximum number of 'attempts'. The player guesses a letter ('Guesses')which are sent to the `make_move` endpoint which will reply
with either: 'Good Guess! word has a <guess letter>' , 'you win' (if all the letters in the word have been guessed, or 'game over' (if the maximum
number of attempts is reached).
A player can play multiple games at a time. Each game can be retrieved or played by using the path parameter
`urlsafe_game_key`.
Scoring: The highest score a player can get is the maximum number of attempts for the game. The score for the player is 
the number of attempts remaining for the player.
When a player guesses a letter that does not occur in the target word, the 'score' decrements the number of attempts remaining. 
When attempts remaining reaches 0, the player has lost the game. 
If the player is able to guess all the letters in the target word, the player has won the game. A high score indicates 
the player has won the game in fewer guesses.

##Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.

##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will 
    raise a ConflictException if a User with that user_name already exists.
    
 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_name, attempts
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not. Also adds a task to a task queue to update the average moves remaining
    for active games.
     
 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.
    
 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, guess
    - Returns: GameForm with new game state.
    - Description: Accepts a 'guess' and returns the updated state of the game.
    If this causes a game to end, a corresponding Score entity will be created.
    
 - **get_scores**
    - Path: 'scores'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all Scores in the database (unordered).
    
 - **get_user_scores**
    - Path: 'scores/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms. 
    - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.
    
 - **get_active_game_count**
    - Path: 'games/active'
    - Method: GET
    - Parameters: None
    - Returns: StringMessage
    - Description: Gets the average number of attempts remaining for all games
    from a previously cached memcache key.

 - **get_user_games**
    - Path: 'games/user/get_games'
    - Method: GET
    - Parameters: user_name, email (optional)
    - Returns: GameForms
    - Description: Returns all active games for the user,(i.e) games that are not over, or cancelled.
 
 - **cancel_game**
    - Path: 'game/{urlsafe_game_key}/cancel_game
    - Method:PUT
    - Parameters: urlsafe_game_key
    - Returns: StringMessage
    - Description: Returns 'Game Cancelled' is the game was successfully cancelled or 'Game Over! cannot be cancelled'.
    
 - **get_high_scores**
    - Path: 'scores/high_scores'
    - Method: GET
    - Parameters: num_scores 
    - Returns: ScoreForms
    - Description: Accepts an integer value num_scores (n) and returns the n highest scores
  
 - **get_user_rankings**
    - Path: 'rankings'
    - Method: GET
    - Parameters: None
    - Returns: RankingForms
    - Description: Returns rankings of all the users, RankingForm contains the percentage of wins and the average scores for each player
    
 - **get_game_history**
    - Path: 'game/history/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameHistoryForms
    - Description: Accepts an urlsafe_game_key and returns GameHistoryForms that contains the guessed letter and whether or not it is present in the target word
     
##Models Included:
 - **User**
    - Stores unique user_name and (optional) email address.
    
 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.
    
 - **Score**
    - Records completed games. Associated with Users model via KeyProperty.
    
##Forms Included:
 - **GameForm**
    - Representation of a Game's state (urlsafe_key, attempts_remaining,
    game_over flag, message, user_name).
 - **NewGameForm**
    - Used to create a new game (user_name, min, max, attempts)
 - **MakeMoveForm**
    - Inbound make move form (guess).
 - **ScoreForm**
    - Representation of a completed game's Score (user_name, date, won flag,
    guesses).
 - **ScoreForms**
    - Multiple ScoreForm container.
 - **StringMessage**
    - General purpose String container.
 - **RankingForm**
    - Outbound form that contains ranking information for a player.(urlsafe_game_key, performance_index, avg_score)
 - **RankingForms**
    - Multiple RankingForm container
 - **GameHistory**
    - Outbound form that contains game move information (urlsafe_key, letter_guessed, is_present)
 - **GameHistoryForms**
    - Multiple Game history forms
 