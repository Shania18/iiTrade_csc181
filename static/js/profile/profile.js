(function ( $ ) {
    $.fn.cm_user_profile_pic_update = function (options) {
        function randomizer(){
            return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
        }
        let width = this.width();

        function adjustedWidth() {
            return (width/2)-((width%10)/2);
        }
        let thisClass = $(this).attr('class');
        function adjustCircle(){return (thisClass.indexOf('img-circle')>0? 'img-circle':'');}
        console.log();
        return this.each(function() {

            let guid = randomizer();
            $(this).append('<div id="cm-profile-pic_'+guid+'" >' +
                '<form id="cm-profile-pic_'+guid+'_form" method="POST" action="'+options.submit+'" enctype="multipart/form-data">' +
                '<input type="hidden" name="_token" value="'+$('meta[name="csrf-token"]').attr('content')+'">'+
                '<input id="cm-profile-pic_'+guid+'_img-upload" class="hidden" name="image" type="file"><form></div>');
            let div = $('#cm-profile-pic_'+guid+'');
            let element = '<div id="cm-profile-pic_'+guid+'_container" style="text-align:center;">' +
                '<img id="cm-profile-pic_'+guid+'_picture" style="height:'+$(this).height()+'px;width: '+$(this).height()+'px;" class="img-responsive '+adjustCircle()+'"  src="'+options.src+'" alt="User profile picture">' +
                '<a type="button" class="btn-primary" id="cm-profile-pic_'+guid+'_btn" style="background:#4285F4;padding: 0px 10px 0px 10px;border-radius: 10px;z-index:100;">Edit</a>' +
                '</div>';
            div.append(element);
            //margin-left:22px;top:90px;
            $(document).on('click','#cm-profile-pic_'+guid+'_picture',function () {
                $('#cm-profile-pic_'+guid+'_img-upload').click();
            });

            $(document).on('click','#cm-profile-pic_'+guid+'_btn',function (e) {
                switch ($(this).html()){
                    case 'Edit':
                        $('#cm-profile-pic_'+guid+'_img-upload').click();
                        break;
                    case 'Save':
                        $('#cm-profile-pic_'+guid+'_form').submit();
                        break;

                }
            });

            $(document).on('change','#cm-profile-pic_'+guid+'_img-upload',function () {
                var input = this;
                var url = $(this).val();
                var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
                if (input.files && input.files[0]&& (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg"))
                {
                    var reader = new FileReader();

                    reader.onload = function (e) {
                        $('#cm-profile-pic_'+guid+'_picture').attr('src', e.target.result);
                        $('#cm-profile-pic_'+guid+'_btn').html('Save').css('left',''+adjustedWidth()+'px');
                    };
                    reader.readAsDataURL(input.files[0]);
                }else{
                    $('#cm-profile-pic_'+guid+'_picture').attr('src', options.src);
                    $('#cm-profile-pic_'+guid+'_btn').html('Edit').css('left',''+(adjustedWidth()+2)+'px');

                }
            });
        });
    }
}( jQuery ));   