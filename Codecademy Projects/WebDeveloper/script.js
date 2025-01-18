let humanScore = 0;
let computerScore = 0;
let currentRoundNumber = 1;

// Write your code below:
const generateTarget = () => {
  let randomNumber = Math.floor(Math.random() * 10)
  return randomNumber
}

// Create a compareGuesses() function. This function: Has three parameters representing the user (human) guess, a computer guess, and the secret target number to be guessed. Determines which player (human or computer) wins based on which guess is closest to the target. If both players are tied, the human user should win. Return true if the human player wins, and false if the computer player wins.

const compareGuesses = (humanGuess, computerGuess, targetNumber) => {
  let humanDifference = Math.abs(targetNumber - humanGuess)
  let computerDifference = Math.abs(targetNumber - computerGuess)
  if (humanDifference <= computerDifference) {
    return true
  } else {
    return false
  }  
}

// Create an updateScore() function. This function: Has a single parameter. This parameter will be a string value representing the winner. Increases the score variable (humanScore or computerScore) by 1 depending on the winner passed in to updateScore. The string passed in will be either 'human' or 'computer'. Does not need to return any value.

const updateScore = winner => {
  if (winner === 'human') {
    humanScore++
  }else if (winner === 'computer') {
    computerScore++
  }
}

// Create an advanceRound() function. This function: Increments the round number by 1. This function will be called at the end of each round.

const advanceRound = () => {
  currentRoundNumber++
}

