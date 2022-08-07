eel.setup()

eel.expose(updateImageSrc)
function updateImageSrc(val, id) {
  let elem = document.getElementById(id);
  if (val == "") 
  {
    elem.src = "";
  }
  else
  {
    elem.src = "data:image/jpeg;base64," + val;
  }
  
}

eel.expose(updateTextSrc)
function updateTextSrc(val,id) {
  document.getElementById(id).innerHTML = val;
}
eel.expose(updateImageSrc)
function updateImageSrc(val, id) {
  let elem = document.getElementById(id);
  elem.src = "data:image/jpeg;base64," + val;
}

function py_video() {
   eel.video_feed()()
}

let captureActive = true;

$(window).keypress(function(e) {
  if (e.key === ' ') {
    if (captureActive) {
      eel.stop_video_feed();
      captureActive = false;
    } else {
      eel.restart_video_feed();
      captureActive = true;
    }
  }
});

eel.expose(get_Option)
function get_Option() {
  selectedOption = $('#idOption').val()
  return selectedOption;
}


eel.expose(get_Value)
function get_Value(id) {
  selectedVal= document.getElementById(id).innerHTML
  return selectedVal;
}




