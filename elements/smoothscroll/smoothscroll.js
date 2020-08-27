$(document).ready(function(){
  var $root = $('html, body');

  $('a[href^="#"]').click(function (event) {
    event.preventDefault();
      $root.animate({
          scrollTop: $( $.attr(this, 'href') ).offset().top
      }, 1000);

      //return false;
  });
});
