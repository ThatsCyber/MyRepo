document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('.login-container button');
  
    button.addEventListener('mousedown', function() {
      button.classList.add('active');
    });
  
    button.addEventListener('mouseup', function() {
      button.classList.remove('active');
      button.classList.remove('dragged');
    });
  
    button.addEventListener('mouseleave', function() {
      if (button.classList.contains('active')) {
        button.classList.add('dragged');
      }
    });
  
    button.addEventListener('mouseenter', function() {
      if (button.classList.contains('dragged')) {
        button.classList.remove('dragged');
      }
    });
  
    // Ensure the button returns to its original color when the mouse is released anywhere on the document
    document.addEventListener('mouseup', function() {
      button.classList.remove('active');
      button.classList.remove('dragged');
    });
  });