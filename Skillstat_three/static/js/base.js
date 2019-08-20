function set_model_width() {
    let width = $('body').outerWidth();
    $('.model').outerWidth(width);
}

function set_form_position() {
    let width = $('body').outerWidth();
    let width2 = $('.s-form').outerWidth();
    $('.s-form').offset({left: (width - width2) / 2});
}

function set_wrapper_height(){
    let height= $('body').outerHeight();
    $('.content-wrapper').outerHeight(height);
}

set_form_position();
set_wrapper_height();

$('.left-add-skill').click(function () {
    set_model_width();
    $('.add-skill').show();
    $('.model').show();
});

$('.level>.dropdown-item').click(function () {
    let value = $(this).text();
    $('.skill-level').text(value);
    $('#level').val(value);
});

$('.category>.dropdown-item').click(function () {
    let value = $(this).text();
    $('.skill-category').text(value);
    $('#category').val(value);
});

$('.add-skill .submit').click(function () {
    let name = $('.add-skill #validationServer01').val();
    let level = $('.add-skill #level').val();
    let category = $('.add-skill #category').val();
    if (name !== '' && level !== '' && category !== '') {
        $('.add-skill .name-reminder').hide();
        $('.add-skill .level-reminder').hide();
        $('.add-skill .category-reminder').hide();
        $('.add-skill #add-skill').submit();
    } else {
        if (name === '') {
            $('.add-skill .name-reminder').show();
        } else {
            $('.add-skill .name-reminder').hide();
        }
        if (level === '') {
            $('.add-skill .level-reminder').show();
        } else {
            $('.add-skill .level-reminder').hide();
        }
        if (category === '') {
            $('.add-skill .category-reminder').show();
        } else {
            $('.add-skill .category-reminder').hide();
        }
    }
});

$('.last>.cancel').click(function () {
    $('.add-skill,.edit-skill,.model').hide();
    $('tbody .mark').removeClass('mark');
    $('.edit-skill .name-reminder').hide();
    $('.add-skill .name-reminder').hide();
    $('.add-skill .level-reminder').hide();
    $('.add-skill .category-reminder').hide();
});
