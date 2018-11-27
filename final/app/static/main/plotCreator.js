(function($, window, document){

    //Select Limitation
    var lastValidSelection = null;
    var $countyRemaining = $('#metro-remaining');
    var MAXSELECTIONS = 6;

    $('#metro-select').change(function(event) {
        var length = $(this).val().length;
        if (length > MAXSELECTIONS) {
          $(this).val(lastValidSelection);
        } else {
          lastValidSelection = $(this).val();
          $countyRemaining.text(MAXSELECTIONS - length);
        }
    });


    //Filter Select
    $("#metro-filter").on('change keyup', function(event){
        var filterText = $(this).val().toUpperCase().split(', ');
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
       for(var i in [1, 2, 3, 4, 5, 6, 7]) {
           $('#metro-'+i).empty();
       }
       $.ajax({
            type: 'GET',
            url: "/metro",
            data: {'metros': JSON.stringify($('#metro-select').val())},
            dataType: 'json',
            success: function(input){
                displayPlot(input['line']);
                displayCircle(input['circle']);
            }
        });

    });

    function displayCircle(input){
        var filteredData = _.groupBy(input, 'sort_by');
        var metro = 1;
        for(var ele in filteredData) {
            var data = [];
            values = _.map(filteredData[ele], function (d) {
                return d.population;
            });
            labels = _.map(filteredData[ele], function (d) {
                return d.county;
            });
            data.push({
                values: values,
                labels: labels,
                hoverinfo: "label+percent+value",
                hole: .4,
                type: "pie"
            });
            var layout = {"title":filteredData[ele][0]['metro']};
            Plotly.newPlot(document.getElementById('metro-'+metro++), data, layout);
        }
    }


    function displayPlot(input){
        var filteredData = _.groupBy(input, 'sort_by');
        var data = [];
        var labelData = [];
        for(var ele in filteredData){
            xData = _.map(filteredData[ele], function(d){ return d.year});
            yData = _.map(filteredData[ele], function(d){ return d.population});
            data.push({
                x: xData,
                y: yData,
                type: 'scatter',
                mode: 'lines+markers',
                marker:{
                    size: 10
                }
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
                text: filteredData[ele][0]['sort_by'].split(/[-,]/)[0] + ' ' + yData[0].toLocaleString(),
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
            margin: {
              l: 100,
              r: 100
            },
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

        var VIZ = document.getElementById('viz');
        Plotly.newPlot(VIZ, data, layout);
    }
}(window.jQuery, window, document));


