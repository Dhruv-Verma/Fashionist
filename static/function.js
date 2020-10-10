// Code By Webdevtrick ( https://webdevtrick.com )
var $header_top = $('.header-top');
var $nav = $('nav');

$header_top.find('a').on('click', function() {
  $(this).parent().toggleClass('open-menu');
});

$('#fullpage').fullpage({
  //sectionsColor: ['#fff', '#348899', '#ff8b20', '#ff5757', '#ffd03c'],
  sectionSelector: '.vertical-scrolling',
  navigation: true,
  slidesNavigation: true,
  controlArrows: false,
  anchors: ['firstSection', 'secondSection', 'thirdSection', 'fourthSection', 'fifthSection'],
  menu: '#menu',

  afterLoad: function(anchorLink, index) {
    $header_top.css('background', 'rgba(0, 47, 77, .3)');
    $nav.css('background', 'rgba(0, 47, 77, .25)');
    if (index == 5) {
        $('#fp-nav').hide();
      }
  },

  onLeave: function(index, nextIndex, direction) {
    if(index == 5) {
      $('#fp-nav').show();
    }
  },

});


var fileHolder = document.getElementById("file-holder");
var fileList = [];
var counter = 0
var mainHolder = document.getElementById("image-holders")
fileHolder.addEventListener('change', function(evnt) {
  for (var i = 0; i < fileHolder.files.length && fileList.length < 10; i++) {
    //fileList.push(fileInput.files[i])
    
    let num = counter + 1;
    counter += 1;
    let reader = new FileReader()
    
    reader.addEventListener('load', (event) => {
      const res = event.target.result
      var image = new Image()
      if (fileList.length < 10) {
        //var holder = '<div class="col-md-2 col-sm-3 col-3 mt-3 ml-3"><button id="cross" data-number=' + '"' + num + '"' + '>X</button>'
        var holder = '<div class="col mt-2 ml-2"><button id="cross" data-number=' + '"' + num + '"' + '>X</button>'
        holder += ('<img src=' + event.target.result + ' data-number=' + '"' + num + '"' + ' style="max-width: 180px; max-height: 180px; width: 100%;" class="img-fluid rounded mx-auto d-block" /></div>')
        mainHolder.innerHTML += holder
        if (fileList.length < 10) fileList.push([num, event.target.result])
        $('button#cross').click(function() {
    
          //console.log("VAU")//
          let t = $(this).data('number')
          console.log(t)
          $(this).parent().remove()
          for (var i = 0; i < fileList.length; i++) {
            if (fileList[i][0] == t) {
              fileList.splice(i, 1)
            }
          }
        })
      }
      
      //console.log(holder)
    })
    reader.readAsDataURL(fileHolder.files[i])
  }
})


// Uploading and Checking Loop
var isUploaded = false

var uploadBtn = document.getElementById("upload-button")
var skipBtn = document.getElementById("skip-button")

uploadBtn.addEventListener('click', function() {
  if (!isUploaded) {
    uploadBtn.setAttribute("disabled", "")
    skipBtn.setAttribute("disabled", "")
  } 
}) 

skipBtn.addEventListener('click', function() {
  if (!isUploaded) {
    uploadBtn.setAttribute("disabled", "")
    skipBtn.setAttribute("disabled", "")
  } 
}) 
