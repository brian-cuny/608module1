(function($, window, document){

    //Select Limitation
    var lastValidSelection = null;
    var $countyRemaining = $('#metro-remaining');

    $('#metro-select').change(function(event) {
        var length = $(this).val().length;
        if (length > 10) {
          $(this).val(lastValidSelection);
        } else {
          lastValidSelection = $(this).val();
          $countyRemaining.text(10 - length);
        }
    });


    //Filter Select
    $("#metro-filter").on('change keyup', function(event){
        var filterText = $(this).val().toUpperCase().split(', ');
        console.log(filterText);
        $('option').each(function(){
            $(this).show();
            for(var filter in filterText){
                if($(this).text().toUpperCase().indexOf(filterText[filter]) < 0){
                    $(this).hide();
                    break;
                }
            }
        });
    });


    //AJAX Query
    $('#submit').on('click', function(e){
       e.preventDefault();
       $.ajax({
            type: 'GET',
            url: "/metro",
            data: {'metros': JSON.stringify($('#metro-select').val())},
            dataType: 'json',
            success: function(data){
                displayPlot(data);
            }
        });

    });


    function displayPlot(data){
        var filteredData = _.groupBy(data, 'sort_by');
        var data = [];
        var labelData = [];
        for(var ele in filteredData){
            xData = _.map(filteredData[ele], function(d){ return d.year});
            yData = _.map(filteredData[ele], function(d){ return d.population});
            data.push({
                x: xData,
                y: yData,
                type: 'scatter',
                mode: 'lines'
            });
            data.push({
                x: [xData[0], xData[xData.length-1]],
                y: [yData[0], yData[yData.length-1]],
                type: 'scatter',
                mode: 'markers',
                marker:{
                    color: 'black',
                    size: 14
                }

            });

            labelData.push({
                xref: 'paper',
                x: 0.05,
                y: yData[0],
                xanchor: 'right',
                yanchor: 'middle',
                text: filteredData[ele][0]['sort_by'] + ' ' + yData[0].toLocaleString(),
                showarrow: false,
                font: {
                    family: 'Arial',
                    size: 16,
                    color: 'black'
                }
            });
            labelData.push({
                xref: 'paper',
                x: 0.95,
                y: yData[yData.length-1],
                xanchor: 'left',
                yanchor: 'middle',
                text: yData[yData.length-1].toLocaleString(),
                font: {
                    family: 'Arial',
                    size: 16,
                    color: 'black'
                },
                showarrow: false
            });

        }

        var layout = {
            showlegend: false,
            xaxis: {
                showline: true,
                showgrid: false,
                showticklabels: true,
                linecolor: 'rgb(204,204,204)',
                linewidth: 2,
                autotick: false,
                ticks: 'outside',
                tickcolor: 'rgb(204,204,204)',
                tickwidth: 2,
                ticklen: 5,
                tickfont: {
                  family: 'Arial',
                  size: 12,
                  color: 'rgb(82, 82, 82)'
                }
            },
            yaxis: {
                showgrid: false,
                zeroline: false,
                showline: false,
                showticklabels: false
            },
            annotations: [
                {
                  xref: 'paper',
                  yref: 'paper',
                  x: 0.0,
                  y: 1.05,
                  xanchor: 'left',
                  yanchor: 'bottom',
                  text: 'Population Change by Metro Area',
                  font:{
                    family: 'Arial',
                    size: 30,
                    color: 'rgb(37,37,37)'
                  },
                  showarrow: false
                },
            ]
        };

        layout.annotations = $.extend(layout.annotations, labelData);
        console.log(layout);

        var VIZ = document.getElementById('viz');
        Plotly.newPlot(VIZ, data, layout);
    }
}(window.jQuery, window, document));

    // function displayPlot(data){
    //     var filteredData = _.groupBy(data, 'sort_by');
    //         data = [];
    //         for(var ele in filteredData){
    //             data.push({
    //                 x: _.map(filteredData[ele], function(d){ return d.year}),
    //                 y: _.map(filteredData[ele], function(d){ return d.population}),
    //                 name: filteredData[ele][0]['sort_by']
    //             });
    //         }
    //
    //         var VIZ = document.getElementById('viz');
    //         Plotly.newPlot(VIZ, data);
    // }