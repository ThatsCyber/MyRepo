// Write your function here:
const howOld = (age, year) => {
  const currentYear = 2024;
  const birthYear = currentYear - age
  const yearDifference = year - currentYear;
  const newAge = age + yearDifference;

  
  if (year > currentYear) {
    return `You will be ${newAge} in the year ${year}`

  }else if (year < birthYear) {
    return `The year ${year} was ${birthYear - year} years before you were born`
  }else if (year < currentYear) {
    return `You were ${newAge} in the year ${year}`
  }



}
  console.log(howOld(31, 2023))