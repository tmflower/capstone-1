MAJOR ISSUES:

-When the first or last letter appears more than once in a word, it is revealed along with the first or last. I thought my "if statements" in the template were written to only reveal the first and last using Jinja filters (also tried using index[0] and [length-1] but got same result). This is especially problematic when the extra letter provided by the hint (letter #3) is already showing.

-startGame function runs on every click (not just the selected button) and re-runs automatically over and over again. WHY??? This also resets the score, even though a new game is not started.
        FIXED: reload was initiated every time game started; placed button for startGame function on same page as game to resolve; also needed to add another clearInterval(timer) to stop countdown if user guesses correctly (not just when countdown hits 0)

-Session score prints accurately in terminal but not in UI, even though using the exact same variable name. Session score needs to reset to 100 at each new game start, but first need to access it to save to user account.
        FIXED: partly from fixing first issue, but also added a "get results" button 



OTHER ISSUES:

-Form fields do not clear when error excepted for same username...should they or can they?
        FIXED: added empty strings at form.username.data and form.password.data

-I can log in as a second user when a user is already logged in (same device, same browser)...should that be able to happen? What does that mean for the Flask session? Does the second user bump the first one?

-My variable "synonyms" returns a list when used standalone, but renders as something else that looks like a dictionary when I try to use this variable in the game-play template; when I try to iterate using "for synonym in word.synonyms" it iterates over each individual character in each synonym. I found a workaround by using synonyms as a separate variable, not as a part of the Word object, and that way I can iterate over a list of synonyms to display them on the page. It works, I'm just not sure if it's the right way to do it.

-I have a TON of repetition in my hint functions in app.js; I'm sure this can be refactored but I'm not sure how to go about it (or how important it is to focus on that).



NEXT STEPS:

-Set up points so that they save to the db under logged in user
    DONE!
-Modify templates so that response is accurate for logged in vs. not logged in user
    DONE!
-Create leaderboard & write logic to show highest scoring players
    DONE!
-Filter out unwanted words (multi-word and hyphenated responses)
    DONE!
-Change starting hints so that it is actually possible to get 100 points (currently not really possible)
    DONE!
-Add rank column to leaderboard.
    DONE! (also had to add rank to User model/table)
-Add player ranking & cumulative points (for logged-in users) to game finish screen...could also show rank out of total number of players but still need to get that number.
    DONE!
-Connect words to users using users_words table
    DONE!
-Add button for user to see all their words
    DONE!
-Add anchor tags to word at game finish; link to info about word & word lookup
    DONE!



NEXT NEXT STEPS:

-Add error handling (for when same word comes up that's already in db)
    DONE! (I think...all I did was redirect to reload the page which will fetch a new word. Is that legit?)
-Write tests
-Improve styling


