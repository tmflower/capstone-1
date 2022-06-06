let points;

function startGame() {    
    points = 100;
    $('#points').text(`Your points: ${points}`)         
    let counter = 10; 
    const timer = setInterval(function(){              
        console.log(counter);
        $('#timer').text(`${counter}`);
        counter--;
        if (counter === 0) {
            clearInterval(timer);
            console.log('timer has stopped!')
            score = 0;
            getScore();
            location.replace('/game/finish');
        }
    }, 1000);
}

// const playBtn = $('#play-btn');
// playBtn.on('click', startGame());
// $('#replay').on('click', startGame());


const $guessForm = $('#check-guess')
const $guess = $('#guess')

$guessForm.on('submit', checkGuess);

async function checkGuess(evt) {
    evt.preventDefault();
    let guess = $guess.val();
    console.log(guess)

    const resp = await axios.get(`/game/check-guess`, { params: { guess: guess } });
    console.log(resp)
    response = resp.config.params.guess
    console.log(response)

    let mysteryWord = $('#mystery-word').text()

    if (guess === mysteryWord) {
        $('#feedback').text("You guessed it!");
        getScore();
        location.assign('/game/finish')
    }

    else {
        $('#feedback').text("Sorry, that's not it.");  
        $guessForm.trigger('reset')
    }    
}

const $hint1 = $('#hint-1');
$hint1.on('click', showHint1);

function showHint1() {
    
    const $definition = $('#definition');
    if (points === 100) {
        $definition.removeClass('invisible');
        points -= 50;
        $('#points').text(`Your points: ${points}`)
        $hint1.prop('disabled', true);
    }
    else if (points === 50) {
        $definition.removeClass('invisible');
        points -= 25;
        $('#points').text(`Your points: ${points}`)
        $hint1.prop('disabled', true);
    }
    else if (points === 25) {
        $definition.removeClass('invisible');
        points -= 15
        $('#points').text(`Your points: ${points}`)
        $hint1.prop('disabled', true);
    }
}

const $hint2 = $('#hint-2')
$hint2.on('click', showHint2);

function showHint2() {
    const $synonyms = $('#synonyms');
    if (points === 100) {
        $synonyms.removeClass('invisible');
        points -= 50;
        $('#points').text(`Your points: ${points}`)
        $hint2.prop('disabled', true);
    }
    else if (points === 50) {
        $synonyms.removeClass('invisible');
        points -= 25;
        $('#points').text(`Your points: ${points}`)
        $hint2.prop('disabled', true);
    }
    else if (points === 25) {
        $synonyms.removeClass('invisible');
        points -= 15;
        $('#points').text(`Your points: ${points}`)
        $hint2.prop('disabled', true);
    }
}

const $hint3 = $('#hint-3')
$hint3.on('click', showHint3);

function showHint3() {
    const $firstLetter = $('#first-letter');
    if (points === 100) {
        $firstLetter.removeClass('invisible');
        points -= 50;
        $('#points').text(`Your points: ${points}`)
        $hint3.prop('disabled', true);
    }
    else if (points === 50) {
        $firstLetter.removeClass('invisible');
        points -= 25;
        $('#points').text(`Your points: ${points}`)
        $hint3.prop('disabled', true);
    }
    else if (points === 25) {
        $firstLetter.removeClass('invisible');
        points -= 15;
        $('#points').text(`Your points: ${points}`)
        $hint3.prop('disabled', true);
    }
}


function getScore() {
    let score = points;
    const dict_values = {score, score};
    const s = JSON.stringify(dict_values);
    console.log(s);
    // window.alert(s);
    $.ajax({
        url:'/game/get-score',
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(s)});
}
