
  $(document).ready(function(){

    $(document).on('click', 'a.dropdown-toggler', function(e){
      e.preventDefault();
      let dropdownName = $(this).attr("data-dropdown");
      $('ul[data-dropdown-name="' + dropdownName + '"]').toggle();
      return false;
    })

    $(document).on('click','#mobile-nav-toggle',function(e) {
        $('div.mobile-nav').toggleClass('show');
    });

    $(document).on('click', '.scrollbox ul li a',function(e) {

        if ( ! ($( this ).hasClass( "dropdown-toggler" )) ) {
            $('div.mobile-nav').toggleClass('show');
        }

    });



    if( $('.secondary-nav').length) {


    var element_position = $('.secondary-nav').offset().top-80;
    var fixed = false;

    $(window).on('scroll', function() {
      var y_scroll_pos = window.pageYOffset;
      var scroll_pos_test = element_position;

      if(y_scroll_pos > scroll_pos_test && fixed == false) {
          fixed = true;
          $('.secondary-nav').addClass('fixed');
          $('.secondary-nav p.logo').fadeTo(300, 1);
      }

      if(y_scroll_pos < scroll_pos_test && fixed == true) {
          fixed = false;
          $('.secondary-nav').removeClass('fixed');
          $('.secondary-nav p.logo').fadeTo(300, 0);

      }
    });

    }

  });
