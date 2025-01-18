// Calculating Function
function displayNumber (number) {
  document.getElementById("input1").value += number;
}

function equalSign () {
  let input1 = document.getElementById("input1").value;
  let result = eval(input1);
  document.getElementById("input1").value = result;
}

function clearScreen () {
  document.getElementById("input1").value = "";
}

// Things to be done:
// Slice the last number of multiple numeric inputs
// Make operators not display more than once, including the decimal point
// Change color of the top row and right column of the calculator