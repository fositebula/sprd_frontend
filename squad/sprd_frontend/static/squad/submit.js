var $pacUrl = $('#device-type').change( function () {
    var nodes = $('#pac-node-'+$(this).val()).data('nodes').split(',');
    var $pac_node = $('#pac-node');
    $pac_node.children().remove();
    for (n in nodes){
        $('<option value='+nodes[n]+'>'+nodes[n]+'</option>').appendTo($pac_node);
    }

    $('#submit').on('click', function () {
        var verify_url = $('#verify-url').val();
        if (verify_url == ''){
            var issubmit = confirm('你确定要提交一个关于daily的测试吗?如果不是请填写verify URL.')
            if(!issubmit){
                return false;
            }
        }

    });
});

$('#switch').click(function () {
        console.log(123);
        $('#vts-models-select').toggle();
        $('#vts-models-input').toggle();
    });