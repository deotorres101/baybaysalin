var preview = $('.preview');
var label = $('.upload-card');
var inputFile = $('[type=file]');
var deleteButton = $('.delete-button');

<<<<<<< HEAD
=======

>>>>>>> 8ce34fd73fd3bdd38c4be121cf2ec9c4f51d14f1
$(document).ready(function() {
    inputFile.on('change', function() {
        const file = inputFile.get(0).files[0];
        if(file) {
    
            var  reader = new FileReader();
            reader.onload = function() {
                preview.attr('src', reader.result);
            }
            reader.readAsDataURL(file);
            label.addClass('shown');
<<<<<<< HEAD
            inputFile.prop('disabled', false);
        }
    });
    
=======

            //need to disable this. Flask can't read the uploaded file
            //inputFile.prop('disabled', true);
        }
    });

>>>>>>> 8ce34fd73fd3bdd38c4be121cf2ec9c4f51d14f1
    deleteButton.on('click', function() {
        preview.attr('src', '');
        label.removeClass('shown');
        inputFile.prop('disabled', false);
    });

});