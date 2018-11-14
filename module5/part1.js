(function($, window, document){
    $('#submit').click(function(e){
        e.preventDefault();
        let toRet = '';
        let reverse = $('#reverse').val();
        for(let i = reverse.length; i >= 0; i--){
            toRet += reverse.charAt(i);
        }
        $('#reverse-text').text(toRet);
    });

    $('#submit-2').click(function(e){
       e.preventDefault();
       let value = Number($('#number').val());
       let $table = $('#multi-table');
       $table.text('');
       if(!isNaN(value)) {
           for (let i = 1; i < 5; i++) {
               let toAdd = '<tr>';
               for (let j = 1; j < 6; j++) {
                   toAdd += '<td>' + (value * i * j) + '</td>';
               }
               toAdd += '</td>';
               $table.append(toAdd);
           }
        }
    });

}(window.jQuery, window, document));