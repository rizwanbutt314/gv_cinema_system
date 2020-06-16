define([
    'jquery',
    'backbone-collections-users',
    'backbone_paginator_view',
    'search_sort_paginate_helpers',
    'common'
], function () {
    var user_id = $('.user_detail').data('id');
    $.each($(document).find('.date'),function (k,v) {
        $(v).text(localizeTime($(v).data('date')))
    });

    function trialPeriod(date) {
        var trial_date = '';
        localizeTime(date);
        var current_date = moment(new Date()),
            trial_date = moment(date),
            days = trial_date.diff(current_date,'days');
        return 'In '+days+'days ('+localizeTime(date)+')';
    }

    $('.trial_date').text(trialPeriod($('.trial_date').data('date')));

    $(document).on('submit-success', '#remote-modal form.edit-user', function (event,data) {
        $('#remote-modal').modal('hide');
        var _msg = gettext('Pending setup');
        var tf_status = data['two_factor_enabled'] == true ? '' : `(${_msg})`;
        data['use_2fa'] = data['use_2fa'] == true ? gettext('On')+ ' '+tf_status : gettext('Off');
        $.each(data,function (key,value) {
            $(document).find('span[data-name='+key+']').text(value)
        });
        if (data['is_account_owner']) {
            $(document).find('span[data-name="permission_level"]').text('Admin (Account Owner)')
        }
    });

    var device_groups_name = [];
    $('#remote-modal').on('click', '.add-permission', function () {
         var device_groups = [];
             device_groups_name = [];
        $('#permission_form :checkbox:checked').each(function (i, v) {
            device_groups.push($(v).data('id'));
            device_groups_name.push($(v).data('name'))
        });
        $('input[name="resources_pk"]').val(device_groups.toString());
    });

    $(document).on('submit-success', '#remote-modal .permission_form', function (event,data) {
        $('#remote-modal').modal('hide');
        var group_el = $('ul.device_groups');
            group_el.html('');
        $.each(device_groups_name,function (k,v) {
            group_el.append('<li>'+v+'</li>');
        });
        device_groups_name = [];
    });

    $(document).on('keyup', '#permission_form input[name="devicegroups-search"]', function (el) {
        var search_value = $(this).val().toLowerCase();
        $(".device_groups_listing label").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(search_value) > -1)
        });
    });

    var clip = new Clipboard('.copy');
    clip.on('success',function (e) {
        notifierPopup({
            element:'.user_detail',
            message:$(e.trigger).data('message')
        });
    });

    $('#remote-modal').on('click', '.delete-user,.reset-password', function () {
        $('#remote-modal').find('.modal-content').load($(this).data('load-url'), function () {
        });
    });

    $(document).on('submit-success', '#remote-modal form.edit-user,#remote-modal form.reset-password, #remote-modal form.user-delete, #permission_form', function (data) {
        $('#remote-modal').modal('hide');
    });

    $(document).on('submit-success', '#remote-modal form.user-delete', function (data) {
        $('#remote-modal').modal('hide');
        window.location.replace("/usermanagement");
    });

    $(document).on('click', '#two-fa-reset', function() {
        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        $.post('2fa/reset',
            {
                'csrfmiddlewaretoken': CSRFtoken,
                'username': $('input[name="username"]').val()
            },
            function(result) {
                $('.two-fa-action').html('Pending setup').addClass('pending')
        });
    });

    $(document).on('change', '.checkbox-onoff-switch-small input[type="checkbox"]', function () {
        $('.checkbox-onoff-switch-small').find('strong').each(function(){
            $(this).toggle()
        });
        var hidden_model_field = 'input[type="hidden"][name="'+$(this).attr('name')+'"]';
        if($(this).is(":checked")){
            $(hidden_model_field).prop('disabled',true);
        }
        else{
            $(hidden_model_field).prop('disabled',false);
        }
    });

    $(document).on('click','.key_gen a',function () {

        var $generate_link = $(this);
        var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
        var $input = $('input[name=api_token]');
        var $copy_btn = $input.closest('.input-group').find('.input-group-btn');
        if($generate_link.hasClass('invalidate_key')){
            $.ajax({
                type: 'delete',
                url: '/usermanagement/api/'+user_id+'/api_token',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken)
                },
            }).success(function (data) {
                $generate_link.removeClass('invalidate_key').addClass('generate_key').text(gettext('Generate API Key'));
                $input.val(null);
                $copy_btn.css('display', 'none');
            }).error(function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR)
            });
        }else{
            $.ajax({
                type: 'post',
                url: '/usermanagement/api/'+user_id+'/api_token',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken)
                },
            }).success(function (data) {
                $input.val(data['api_token']);
                $generate_link.removeClass('generate_key').addClass('invalidate_key').text(gettext('Invalidate API Key'));
                $copy_btn.css('display', 'table-cell');
            }).error(function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR)
            })
        }
    });

});
