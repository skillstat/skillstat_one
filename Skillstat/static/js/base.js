$('.left-skill-list').click(function(){
    $.get('/skillPerson/perList/')
})

$('.left-add-skill').click(function () {
    set_model_width();
    $('.add-skill').show();
    $('.model').show();
});