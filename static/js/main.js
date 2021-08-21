var likeBtn = document.getElementsByClassName('likeBtn')
var unlikeBtn = document.getElementsByClassName('unlikeBtn')
/**
 * Easy selector helper function
 */
const select = (el, all = false) => {
el = el.trim()
if (all) {
    return [...document.querySelectorAll(el)]
} else {
    return document.querySelector(el)
}
}

/**
 * Easy event listener function
 */
const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }
    on('click', '.mobile-nav-toggle', function(e) {
        select('#navbar').classList.toggle('navbar-mobile')
        this.classList.toggle('bi-list')
        this.classList.toggle('bi-x')
      })



$(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
        $('#header').addClass('header-scrolled');
} else {
    $('#header').removeClass('header-scrolled');
}
});


// subscribe btn

$('.subscribe-form').submit(function(e){
  e.preventDefault()
  console.log('submiting....')
  var name = document.getElementById('sub-name').value
  var email = document.getElementById('sub-email').value
  if(name == ''){
    var name = document.getElementById('sub-name1').value
    var email = document.getElementById('sub-email1').value
  }
  $.ajax({
    type: "POST",
    url: "subscribe",
    'csrfmiddlewaretoken': '{{ csrf_token }}',
    data: {
      'name': name,
      'email': email
    },
    dataType: "json",

    success: function(data){
      if(data.message1 != ''){
        Swal.fire({
          position: 'top-end',
          text: data.message1,
          icon: 'success',
          showConfirmButton: true,
          timer: 4500
        })
      }else{
      Swal.fire({
        position: 'top-end',
        text: data.message2,
        icon: 'error',
        showConfirmButton: true,
        timer: 4500
      })
    }
    var form = document.getElementsByClassName('subscribe-form')
    for(var i=0; i < form.length; i++){
      form[i].reset();
    }
  },
    error: function(error){
      console.log('error occured')
    }
    
  })
})

AOS.init({
  offset: 200,
  duration: 2000,
  once: true,
});