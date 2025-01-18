// Get elements from HTML
let playerScoreElement = document.getElementById('player-score');
let computerScoreElement = document.getElementById('computer-score');
let computerPickElement = document.getElementById('computer-pick');
let determineWinnerElement = document.getElementById('determine-winner');
let playerPickElement = document.getElementById('player-pick');

let resetButton = document.getElementById('resetbtn');

let playerScore = 0;
let computerScore = 0;

// Add event listeners to buttons
document.getElementById('rock').addEventListener('click', () => playGame('rock'));
document.getElementById('paper').addEventListener('click', () => playGame('paper'));
document.getElementById('scissors').addEventListener('click', () => playGame('scissors'));
resetButton.addEventListener('click', () => resetGame());

function playGame(playerChoice) {
  let computerChoice = getComputerChoice();
  computerPickElement.textContent = 'Computer picked: ' + computerChoice;
  playerPickElement.textContent = 'Player picked: ' + playerChoice;
  
  if (playerChoice === computerChoice) {
    // It's a tie
    determineWinnerElement.textContent = 'It\'s a tie!';
  } else if (
    (playerChoice === 'rock' && computerChoice === 'scissors') ||
    (playerChoice === 'paper' && computerChoice === 'rock') ||
    (playerChoice === 'scissors' && computerChoice === 'paper')
  ) {
    // Player wins
    playerScore++;
    playerScoreElement.textContent = 'Player Score: ' + playerScore;
    determineWinnerElement.textContent = 'Player wins!';
  } else {
    // Computer wins
    computerScore++;
    computerScoreElement.textContent = 'Computer Score: ' + computerScore;
    determineWinnerElement.textContent = 'Computer wins!';
  }
}

function getComputerChoice() {
  const choices = ['rock', 'paper', 'scissors'];
  const randomIndex = Math.floor(Math.random() * 3);
  return choices[randomIndex];
}

function resetGame() {
  playerScore = 0;
  computerScore = 0;
  playerScoreElement.textContent = 'Player Score: ' + playerScore;
  computerScoreElement.textContent = 'Computer Score: ' + computerScore;
  computerPickElement.textContent = 'Computer picked: ';
  determineWinnerElement.textContent = "Let's play!";
  playerPickElement.textContent = 'Player picked: ';
}