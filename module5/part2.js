(function($, window, document){

    let presidents;

    d3.csv('presidents.csv', function(error, data){
       if(error){
           console.log('Error');
       }
       presidents = data;
       let table = d3.select('#presidents');

       table.append('thead').append('tr').html(function(){
           let toRet = '';
           data.columns.forEach(function(ele, index){
              toRet += '<th>' + ele + '</th>';
           });
           return(toRet);
       });

       data.forEach(function(row){
           let toAdd = '';
           for(let key in row){
               toAdd += '<td>' + row[key] + '</td>';
           }
           table.append('tr').html(toAdd);
       });
    });

    $('#president-submit').click(function(e){
       e.preventDefault();
       let selection = $('#president-selection').val();
       let toAdd = $('#results');
       // toAdd.html('');
       for(let ele in presidents){
           if(presidents[ele].Name === selection){
                toAdd.prepend('<p>' + presidents[ele].Name + " " + presidents[ele].Height + " " +
                    presidents[ele].Weight + '</p>');
                return;
           }
       }
       toAdd.prepend('<p>' + selection + ': NOT FOUND</p>');
    });

}(window.jQuery, window, document));