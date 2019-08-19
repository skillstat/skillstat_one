function set_model_width() {
    let width = $('.content-wrapper').outerWidth();
    $('.model').outerWidth(width);
}

function set_form_position() {
    let width = $('body').outerWidth();
    let width2 = $('.s-form').outerWidth();
    $('.s-form').offset({left: (width - width2) / 2});
}

function set_perform_position() {
    let offset = $('table .edit').offset().left;
    $('table .perform').offset({left: offset})
}
set_form_position();
set_perform_position();
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

$('tbody .delete').click(function () {
    let index = $(this).attr('index');
    $.post('/skillPerson/delete/', {'index': index});
    $(this).closest('tr').remove();
});

$('tbody .edit').click(function () {
    set_model_width();
    let $tds = $(this).parents('tr').children('td');
    let index = $(this).attr('index');
    let name = $tds.eq(1).text();
    let level = $tds.eq(2).text();
    let category = $tds.eq(3).text();
    $(this).parents('tr').addClass('mark');
    $('.edit-skill,.model').show();
    $('.edit-skill .skill-id').text(index);
    $('.edit-skill #validationServer01').val(name);
    $('.edit-skill .skill-level').text(level);
    $('.edit-skill .skill-category').text(category);
});

$('.edit-skill .confirm').click(function () {
    let id = $('.edit-skill .skill-id').text();
    let name = $('.edit-skill #validationServer01').val();
    let level = $('.edit-skill .skill-level').text();
    let category = $('.edit-skill .skill-category').text();
    if (name === '') {
        $('.edit-skill .name-reminder').show()
    } else {
        $.post('/skillPerson/edit/', {'id': id, 'name': name, 'level': level, 'category': category});
        $('.add-skill,.edit-skill,.model').hide();
        let $tds = $('tbody .mark').children('td');
        $tds.eq(1).text(name);
        $tds.eq(2).text(level);
        $tds.eq(3).text(category);
        $('tbody .mark').removeClass('mark');
        $('.edit-skill .name-reminder').hide()
    }
    ;

});
// $('.test').click(function () {
//     $.post('/skillPerson/test/', function (test) {
//         console.log(test);
//         for (let i in test) {
//             console.log(test[i]['skill_name']);
//             console.log(test[i]['skill_level']);
//             console.log(test[i]['category']);
//         }
//     })
// });




