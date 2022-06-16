let points;
let timer;
let result;

function startGame() {   
    points = 100;
    $('#points').text(`Your remaining points: ${points}`);         
    let counter = 60;
    $('#active-game').removeClass('invisible');
    $('#game-over').addClass('invisible');
    $('#play-btn').addClass('invisible');
    timer = setInterval(function(){              
        $('#timer').text(`${counter}`);
        counter--;
        if (counter === -1) {
            result = lose;
            clearInterval(timer);
            points = 0;
            $('#points').text(`Your remaining points: 0`);
            getScore();
            endGame();
        }
    }, 1000);
}

const playBtn = $('#play-btn');
playBtn.on('click', startGame);

function endGame() {
    $('#word-info').remove();
    $('#letters').remove();
    $hint1.remove();
    $hint2.remove();
    $hint3.remove();
    $('#definition').remove();
    $('#synonyms').remove();
    $('#syllables').remove();
    $('.hint-cards').remove();
    $guessForm.remove();
    $guess.remove();
    $('#game-over').removeClass('invisible')
    if (result === lose) {
        $('#lose').removeClass('invisible');
        $('#lose').append('<p id="msg">Check your results to see the correct answer.</p>')
        $('#win').remove();
    }
    else {
        $('#win').removeClass('invisible');
        $('#lose').remove();
    }
    $('#replay').removeClass('invisible');
}

$('#results').on('click', getResults);
function getResults() {
    location.replace('/game/finish')
}

$('#replay').on('click', playAgain);
function playAgain() {
    location.replace('/game/play');
}

const $guessForm = $('#check-guess');
const $guess = $('#guess');

$guessForm.on('submit', checkGuess);

async function checkGuess(evt) {
    evt.preventDefault();
    let caps = $guess.val()
    let guess = caps.toLowerCase();

    const resp = await axios.get(`/game/check-guess`, { params: { guess: guess } });
    response = resp.config.params.guess

    let mysteryWord = $('#mystery-word').text()

    if (guess === mysteryWord) {
        result = win;
        clearInterval(timer);
        $('#feedback').text("You guessed it!");
        getScore();
        endGame();
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
        $('#points').text(`Your remaining points: ${points}`)
        $hint1.prop('disabled', true);
    }
    else if (points === 50) {
        $definition.removeClass('invisible');
        points -= 25;
        $('#points').text(`Your remaining points: ${points}`)
        $hint1.prop('disabled', true);
    }
    else if (points === 25) {
        $definition.removeClass('invisible');
        points -= 15
        $('#points').text(`Your remaining points: ${points}`)
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
        $('#points').text(`Your remaining points: ${points}`)
        $hint2.prop('disabled', true);
    }
    else if (points === 50) {
        $synonyms.removeClass('invisible');
        points -= 25;
        $('#points').text(`Your remaining points: ${points}`)
        $hint2.prop('disabled', true);
    }
    else if (points === 25) {
        $synonyms.removeClass('invisible');
        points -= 15;
        $('#points').text(`Your remaining points: ${points}`)
        $hint2.prop('disabled', true);
    }
}

const $hint3 = $('#hint-3')
$hint3.on('click', showHint3);

function showHint3() {
    const $syllables = $('#syllables');
    if (points === 100) {
        $syllables.removeClass('invisible');
        points -= 50;
        $('#points').text(`Your remaining points: ${points}`)
        $hint3.prop('disabled', true);
    }
    else if (points === 50) {
        $syllables.removeClass('invisible');
        points -= 25;
        $('#points').text(`Your remaining points: ${points}`)
        $hint3.prop('disabled', true);
    }
    else if (points === 25) {
        $syllables.removeClass('invisible');
        points -= 15;
        $('#points').text(`Your remaining points: ${points}`)
        $hint3.prop('disabled', true);
    }
}


function getScore() {
    let score = points;
    const dict_values = {score, score};
    const s = JSON.stringify(dict_values);
    $.ajax({
        url:'/game/get-score',
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(s)});
}