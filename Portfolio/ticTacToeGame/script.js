// Initialize game state
let board = Array(9).fill(null);
let currentPlayer = 'X';

// Add event listeners to each box and the reset button
document.querySelectorAll('.box').forEach((box, i) => {
  box.addEventListener('click', () => {
    // If the box is already filled or the game is over, return
    if (board[i] || checkWin(board)) return;

    // Update game state and display
    board[i] = currentPlayer;
    box.textContent = currentPlayer;

    // Check for win or draw
    if (checkWin(board)) {
      document.getElementById('playerText').textContent = `Player ${currentPlayer} wins!`;
    } else if (board.every(cell => cell)) {
      document.getElementById('playerText').textContent = 'Draw!';
    } else {
      // Switch players
      currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
      document.getElementById('playerText').textContent = `Player ${currentPlayer}'s turn`;
    }
  });
});

document.getElementById('reset-btn').addEventListener('click', () => {
  // Reset game state and display
  board = Array(9).fill(null);
  currentPlayer = 'X';
  document.getElementById('playerText').textContent = 'Tic Tac Toe';
  document.querySelectorAll('.box').forEach(box => box.textContent = '');
  
});

// Check for a win
function checkWin(board) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];
  for (let line of lines) {
    if (board[line[0]] && board[line[0]] === board[line[1]] && board[line[0]] === board[line[2]]) {
      return true;
    }
  }
  return false;
}
