MAJOR ISSUES:

-startGame function runs on every click (not just the selected button) and re-runs automatically over and over again. WHY??? This also resets the score, even though a new game is not started.
        FIXED: reload was initiated every time game started; placed button for startGame function on same page as game to resolve; also needed to add another clearInterval(timer) to stop countdown if user guesses correctly (not just when countdown hits 0)

-Session score prints accurately in terminal but not in UI, even though using the exact same variable name. Session score needs to reset to 100 at each new game start, but first need to access it to save to user account.
        FIXED: partly from fixing first issue, but also added a "get results" button 



OTHER ISSUES:

-Form fields do not clear when error excepted for same username...should they or can they?
        FIXED: added empty strings at form.username.data and form.password.data

-I can log in as a second user when a user is already logged in (same device, same browser)...should that be able to happen? What does that mean for the Flask session? Does the second user bump the first one?

-Synonyms returns a list, but renders as a dictionary in template; when I try to iterate using "for synonym in word.synonyms" it iterates over each individual character. Using workaround for now of synonyms as a separate variable in template so I can iterate over a list but this doesn't seem ideal.

-I have a TON of repetition in my hint functions in app.js; can this be refactored?



NEXT STEPS:

-Set up points so that they save to the db under logged in user
-Modify templates so that response is accurate for logged in vs. not logged in user
-Create leaderboard & write logic to show highest scoring players


NEXT NEXT STEPS:

-Add error handling (esp. for when same word comes up that's already in db)
-Write tests
-Improve styling
-Add a "more about this word" lookup option after each round


