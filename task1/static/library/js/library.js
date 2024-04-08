function addClass(elementId, className) {
    var element = document.getElementById(elementId);
    if (element) {
        if (!element.classList.contains(className)) {
            element.classList.add(className);
            console.log("Class '" + className + "' added to element with id '" + elementId + "'");
        } else {
            console.log("Class '" + className + "' already exists on element with id '" + elementId + "'");
        }
    } else {
        console.error("Element with id '" + elementId + "' not found.");
    }
}

function removeClass(elementId, className) {
    var element = document.getElementById(elementId);
    if (element) {
        if (element.classList.contains(className)) {
            element.classList.remove(className)
            console.log("Class '" + className + "' removed to element with id '" + elementId + "'");
        } else {
            console.log("Class '" + className + "' not exists'" + elementId + "'");
        }
    } else {
        console.error("Element with id '" + elementId + "' not found.");
    }
}

function addSlideElements() {
    removeClass('new-step', 'rm-display')
}

function removeSideElements() {
    addClass('new-step', 'rm-display')
}

$("#addbotton").on( "click", function( event ) {
    addSlideElements()
  });

  $("#addbutton2").on( "click", function( event ) {
    addSlideElements()
  });

  $("#closebotton").on( "click", function( event ) {
    removeSideElements()
  });

  $("#saveBookBtn").on( "click", function( event ) {
    location.reload();
    // var fileInput = document.getElementById('file-input');
    // var file = fileInput.files[0];
    // var title = $('#title-book').val();
    // var genre = $('#genre-book').val();
    // var formData = new FormData();
    // formData.append('file', file);
    // formData.append('title', title);
    // formData.append('genre', genre);
    // console.log(formData, "form data")
    // $.ajax({
    //     url: "http://localhost:8000/create-book",
    //     type: "POST",
    //     data: formData,
    //     success: function(response) {
    //         console.log("Success:", response);
    //         location.reload();
    //     },
    //     error: function(xhr, status, error) {
    //         console.error("Error:", error);
    //     }
    // });    
  });

