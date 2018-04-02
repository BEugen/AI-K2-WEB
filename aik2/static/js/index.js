function getdata(url, root, token) {
    $.ajax(
        {
            url: url,
            data: {
                id: 0, 'csrfmiddlewaretoken': token
            },
            timeout: 300000,
            type: 'POST',
            beforeSend: function () {
            },
            success: function (data) {
                drawdata(data, root);
                window.setTimeout(function () {
                   getdata(url, root, token);
                }, 30000);
            },
            error: function() {
                window.setTimeout(function () {
                    getdata(url, root, token);
                }, 30000);
            }
        });
}

function getstat(url, token) {
    $.ajax(
        {
            url: url,
            data: {
                id: 0, 'csrfmiddlewaretoken': token
            },
            timeout: 300000,
            type: 'POST',
            beforeSend: function () {
            },
            success: function (data) {
                drawstat(data);
                window.setTimeout(function () {
                   getstat(url, token);
                }, 108000);
            },
            error: function() {
                window.setTimeout(function () {
                    getstat(url, token);
                }, 108000);
            }
        });
}

function drawstat(data)
{
  let sm = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
  for(let i=0; i < 3; i++) {
      let ind = 0;
      for(let y=-1; y < 5; y++)
      {
          let v = data[i][y.toString()];
          if( v != null) {
              $("#s" + (i + 1) + "_" + y).text((v/60).toFixed(2) + "ч.");
              sm[ind] += v;
          }
          else
          {
              $("#s" + (i + 1) + "_" + y).text("-");
          }
          ind +=1;
      }
  }
  let ind = -1;
  for (let i=0; i < sm.length; i++)
  {
      if(sm[i] !== 0.0) {
          $("#s4" + "_" + ind).text((sm[i]/60).toFixed(2) + "ч.");
      }
      else
      {
          $("#s4" + "_" + ind).text("-");
      }
      ind +=1;
  }

}


function drawdata(data, root)
{
    if((data['predstop'] <= 0.7 && data['idnext'] == null && data['predfull'] > data['predempty'])
        ||data == null || data.length == 0)
         return;
    $("[id^='cnn']", root).each(
        function(){
            $(this).css('fill', '#808286');
            $(this).css('fill-opacity', 0.5);
        });
    $("[id^='cce']", root).each(
        function(){
            $(this).css('fill', '#747474');
        });
    $("[id^='br']", root).each(
        function(){
            $(this).css('display', 'none');
        });
    $("[id^='cp']", root).each(
        function(){
            $(this).css('stroke', '#808286');
            $(this).css('stroke-opacity', 0.5);
            $(this).css('stroke-width', 1.0)
        });
    $("#tspan3649", root).text('???');
    $("#tspan3655", root).text('???');
    $("#tspan3661", root).text('???');
    $("#tspan3667", root).text('???');
    $("#tspan3625", root).text('???');

    $("#tspan3637", root).text('???');
    $("#tspan3620", root).text('???');
    $("#tspan3619", root).text('???');
    $("#tspan3643", root).text('???');

    $("#image9", root).attr('href', 'data:image/jpeg;base64,' + data['img']);
    //$("#image9", root).width(245);
    //$("#image9", root).height(214);
    $("#tspan3631", root).text(data['stamp']);
    $("#tspan3637", root).text(Math.round(data['predstop']*100) + '%');
    $("#tspan3620", root).text(Math.round((1.0 - data['predstop'])*100) + '%');
    $("#cp3", root).css('stroke', '#6ae5ff');
    $("#cp0", root).css('stroke', '#6ae5ff');
    $("#cp3", root).css('stroke-width', strokew(1.0, 12.0, data['predstop']));
    $("#cp0", root).css('stroke-width', strokew(1.0, 12.0, (1.0 - data['predstop'])));
    const cnn1 =  $("#cnn1", root);
    const cnn4 =  $("#cnn4", root);
    if (data['predstop'] > 0.7)
    {
        cnn1.css('fill', '#808286');
        cnn1.css('fill-opacity', 0.5);
        cnn4.css('fill', '#808286');
        cnn4.css('fill-opacity', 0.5);

        return;
    }
    else
    {
        cnn1.css('fill', '#6ae5ff');
        cnn1.css('fill-opacity', 1.0);
        $("[id^='cce']", root).each(
        function(){
            $(this).css('fill', '#32f90a');
        });
        cnn4.css('fill', '#6ae5ff');
        cnn4.css('fill-opacity', 1.0);
    }
    const br = $("[id^='br']", root);
    const cnn2 =  $("#cnn2", root);
    $("#cp4", root).css('stroke', '#6ae5ff');
    if (data['predfull'] > data['predempty']) {
        br.each(
        function(){
            $(this).css('display', 'inline');
        });
        cnn2.css('fill', '#6ae5ff');
        cnn2.css('fill-opacity', 1.0);
        $("#tspan3643", root).text(Math.round(data['predfull']*100) + '%');
        $("#tspan3619", root).text(Math.round(data['predfull']*100) + '%');
        $("#cp4", root).css('stroke-width', strokew(1.0, 12.0, data['predfull']));
        $("#cp1", root).css('stroke', '#6ae5ff');
        $("#cp1", root).css('stroke-width', strokew(1.0, 12.0, data['predfull']));
    }
    else
    {
        br.each(
        function(){
            $(this).css('display', 'none');
        });
        cnn2.css('fill', '#808286');
        cnn2.css('fill-opacity', 0.5);
        $("#tspan3643", root).text(Math.round(data['predempty']*100) + '%');
        $("#tspan3619", root).text(Math.round(data['predfull']*100) + '%');
        $("#cp4", root).css('stroke-width', strokew(1.0, 12.0, data['predempty']));
    }
    if (data['idnext'] != null)
    {
        data = data['idnext'];
        switch (data['nclass']) {
            case 0:
                br.each(
                    function () {
                        $(this).css('display', 'none');
                    });
                $("#cp5", root).css('stroke', '#6ae5ff');
                $("#cp5", root).css('stroke-width', strokew(1.0, 12.0, data['predict0']));
                break;
             case 1:
                $("#cnn5", root).css('fill', '#f13c09');
                $("#cnn5", root).css('fill-opacity', 1.0);
                $("#cp6", root).css('stroke', '#f13c09');
                $("#cp6", root).css('stroke-width', strokew(1.0, 12.0, data['predict1']));
                break;
             case 2:
                $("#cnn7", root).css('fill', '#f13c09');
                $("#cnn7", root).css('fill-opacity', 1.0);
                $("#cp7", root).css('stroke', '#f13c09');
                $("#cp7", root).css('stroke-width', strokew(1.0, 12.0, data['predict2']));
                break;
             case 3:
                $("#cnn6", root).css('fill', '#6ae5ff');
                $("#cnn6", root).css('fill-opacity', 1.0);
                $("#cp8", root).css('stroke', '#6ae5ff');
                $("#cp8", root).css('stroke-width', strokew(1.0, 12.0, data['predict3']));
                break;
             case 4:
                $("#cnn3", root).css('fill', '#6ae5ff');
                $("#cnn3", root).css('fill-opacity', 1.0);
                $("#cp2", root).css('stroke', '#6ae5ff');
                $("#cp2", root).css('stroke-width', strokew(1.0, 12.0, data['predict4']));
                break;
            default:
                break;
        }
        $("#tspan3649", root).text(Math.round(data['predict0']*100)+'%');
        $("#tspan3655", root).text(Math.round(data['predict1']*100)+'%');
        $("#tspan3661", root).text(Math.round(data['predict2']*100)+'%');
        $("#tspan3667", root).text(Math.round(data['predict3']*100)+'%');
        $("#tspan3625", root).text(Math.round(data['predict4']*100)+'%');
    }
}

function strokew(min, max, coeff) {
    return (max-min)*coeff+min;

}

function getdatachart(id, url, chart, options, subscribe, token)
{
     $.ajax(
        {
            url: url,
            data: {
                id: id, 'csrfmiddlewaretoken': token
            },
            timeout: 300000,
            type: 'POST',
            beforeSend: function () {
            },
            success: function (data) {
                drawchart(chart, options, data);
                if(subscribe) {
                    window.setTimeout(function () {
                        getdatachart(id, url, chart, options, subscribe, token);
                    }, 120000);
                }
            },
            error: function() {
                window.setTimeout(function () {
                    getdatachart(id, url, chart, options, subscribe, token);
                }, 120000);
            }
        });
}

function drawchart(chart, options, data) {
    $.plot("#" + chart, [ data[0], data[1], data[2],
        data[3], data[4], data[5]], options);
}