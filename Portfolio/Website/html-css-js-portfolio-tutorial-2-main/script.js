function toggleMenu() {
  const menu = document.querySelector(".menu-links");
  const icon = document.querySelector(".hamburger-icon");
  menu.classList.toggle("open");
  icon.classList.toggle("open");
}

function toggleMenu(){
  const menu = document.querySelector(".menu-links");
  const icon = document.querySelector(".hamburger-icon");
  menu.classList.toggle("open");
  icon.classList.toggle("open");
}

window.addEventListener('scroll', function(){
  const arrow = document.getElementById('scrollToTopArrow');
  if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight){
    arrow.classList.add('show');
  }
  else{
    arrow.classList.remove('show');
  }
});