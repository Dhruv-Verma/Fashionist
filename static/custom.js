$(document).ready(function() {
	$('#pagepiling').pagepiling({
    sectionsColor: ['#f2f2f2', '#4BBFC3', '#7BAABE', 'whitesmoke', '#000']
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

  // Important util functions
  var gender = -1
  var occasion = -1

  var maleBtn = document.getElementById("male-gender")
  var femaleBtn = document.getElementById("female-gender")

  maleBtn.addEventListener('click', function() {
    maleBtn.classList.add('img-glow')
    femaleBtn.classList.remove('img-glow')
    gender = "male"
    window.location.href="#thirdSection"
  })

  femaleBtn.addEventListener('click', function() {
    femaleBtn.classList.add('img-glow')
    maleBtn.classList.remove('img-glow')
    gender = "female"
    window.location.href="#thirdSection"
  })

  function setOccasion(o) {
    occasion = o
    window.location.href="#fourthSection"
  }

  // Uploading and Checking Loop

  var isUploaded = false
  var useFiles = false

  var uploadBtn = document.getElementById("upload-button")
  var skipBtn = document.getElementById("skip-button")
  var submitBtn = document.getElementById("get-predictions")
  var finalStatusText = document.getElementById("finalResultStatus")
  var finalImageHolder = document.getElementById("post-submission")
  var task_id = -1

  uploadBtn.addEventListener('click', function() {
    if (fileList.length < 10) {
      alert("Less than 10 images, upload more!")
    } else {
      useFiles = true
      window.location.href= "#fifthSection"
    }
  }) 

  skipBtn.addEventListener('click', function() {
    useFiles = false
    window.location.href= "#fifthSection"
  }) 

  submitBtn.addEventListener('click', () => {
    var formData = new FormData()
    if (gender == -1) {
        alert("Gender Not Selected!")
        window.location.href="#secondSection"
        return
      }
      if (occasion == -1) {
        alert("Occasion not selected!")
        window.location.href="#thirdSection"
        return 
      }
      formData.append("gender", gender)
      formData.append("occasion", occasion)
    if (useFiles) {
      console.log(fileList)
      formData.append("use_files", true)
      let uploadList = []
      for (let ind= 0; ind < fileList.length; ind++) {
        uploadList.push(fileList[ind][1])
      }
      formData.append('files', uploadList)
      console.log(uploadList)
    } else {
      formData.append('files', [])
      formData.append("use_files", false)
    }
    var request = new XMLHttpRequest()
    request.open("POST", "/getPredictions")
    request.send(formData)
    submitBtn.classList.add('disabled')
    submitBtn.disabled = true
    finalStatusText.innerHTML = "FETCHING RESULT..."
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          // Typical action to be performed when the document is ready:
          let resp = JSON.parse(request.response)
          console.log(resp)
          task_id = resp['job_id']

          checkProgress()
        }
    };
  })

  var check_progress_timeout;
  function checkListener() {
    var data = this.responseText
    console.log("Data", data)
    check_progress_timeout = setTimeout(checkProgress, 2000)
  }

  function checkError(err) {
    console.log('Fetch Error :-S', err);
  }

  function checkProgress() {
    finalStatusText.innerHTML = "PROCESS QUEUED..."
    var checkRequest = new XMLHttpRequest()
    checkRequest.open('GET', '/status/' + task_id.toString())
    checkRequest.send()
    checkRequest.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          // Typical action to be performed when the document is ready:
          let resp = JSON.parse(checkRequest.response)
          console.log(resp)
          if (resp['msg'] == '[started]') setTimeout(checkProgress, 2000)
          else if (resp['msg'] == '[failed]') getFailure()
          else getResult()
        }
    }
  }

  function getResult() {
    var checkRequest = new XMLHttpRequest()
    checkRequest.open('GET', '/result/' + task_id.toString())
    checkRequest.send()
    checkRequest.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          // Typical action to be performed when the document is ready:
          let resp = JSON.parse(checkRequest.response)
          finalStatusText.innerHTML = "Success! Try again!"
          showSuccessImages(resp['short_result'])
          submitBtn.disabled = false
          submitBtn.classList.remove('disabled')
        }
    }
  }

  function getFailure() {
    var checkRequest = new XMLHttpRequest()
    checkRequest.open('GET', '/result/' + task_id.toString())
    checkRequest.send()
    checkRequest.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          // Typical action to be performed when the document is ready:
          let resp = JSON.parse(checkRequest.response)
          finalStatusText.innerHTML = "FAILED! Try again!"
          submitBtn.disabled = false
          submitBtn.classList.remove('disabled')
        }
    }
  }

  function showSuccessImages(imageNames) {
    finalImageHolder.innerHTML = ""
    let imageOptions = imageNames.split('|')
    console.log(imageOptions)
    for (imageOption in imageOptions) {
      finalImageHolder.innerHTML += getImageTag(imageOptions[imageOption])  
    }
    //finalImageHolder
  }

  function getStarting() {
    return `<img src="static/images/`
  }

  function getEnd() {
    return '.jpg")}}" style="height: 200px; max-width: 100%"/>'
  }

  function getImageTag(imageName) {
    console.log(imageName)
    let ImageTag = getStarting() + imageName + getEnd() 
    console.log(ImageTag)
    return ImageTag
  }
});