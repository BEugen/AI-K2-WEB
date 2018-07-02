var tmdata = null;
var tmstat = [];
var achart = null;
var astat = null;

function getdata(url, root, token) {
   astat =  $.ajax(
        {
            url: url,
            data: {
                id: 0, 'csrfmiddlewaretoken': token
            },
            timeout: 100000,
            type: 'POST',
            beforeSend: function () {
            },
            success: function (data) {
                drawinfo(data, root);
                tmdata = window.setTimeout(function () {
                   getdata(url, root, token);
                }, 10000);
            },
            error: function() {
                tmdata = window.setTimeout(function () {
                    getdata(url, root, token);
                }, 10000);
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
                tmstat = window.setTimeout(function () {
                   getstat(url, token);
                }, 108000);
            },
            error: function() {
                tmstat = window.setTimeout(function () {
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
    if(data == null)
         return;
    $("[id^='line']", root).each(
        function(){
            $(this).css('stroke', '#595b5d');
        });

    $("[id^='circle-']", root).each(
        function(){
            $(this).css('stroke', '#595b5d');
            $(this).css('fill-opacity', 0.0);
        });

    $("[id^='br']", root).each(
        function(){
            $(this).css('display', 'none');
        });
    $("[id^='bcircle-']", root).each(
        function(){
            $(this).css('display', 'none');
        });

    $("[id^='cce']", root).each(
        function(){
            $(this).css('fill', '#747474');
        });

    if (data['snnclass'] !== 1) {
        $("#line-0", root).css('stroke', '#eaeaea');
        $("#line-1", root).css('stroke', '#eaeaea');
        $("#circle-0", root).css('stroke', '#eaeaea');
        $("#bcircle-0", root).css('display', 'inline');
        if (data['stop'] <= 0.95) {
            $("[id^='cce']", root).each(
                function () {
                    $(this).css('fill', '#32f90a');
                });
        }
        else
        {
            return;
        }
    }
    const br = $("[id^='br']", root);
    if (data['full'] > data['empty'] && data['snnclass'] !== 1) {
        br.each(
        function(){
            $(this).css('display', 'inline');
        });
    }
    else
    {
        br.each(
        function(){
            $(this).css('display', 'none');
        });
    }
    switch (data['snnclass']) {
        case 0:
            br.each(
                function () {
                    $(this).css('display', 'none');
                });
            break;
        case 1:
            $("#line-6", root).css('stroke', '#f20855');
            $("#circle-4", root).css('stroke', '#f20855');
            $("#bcircle-4", root).css('display', 'inline');
            break;
        case 2:
            $("#line-3", root).css('stroke', '#ff0f3c');
            $("#circle-1", root).css('stroke', '#ff0f3c');
            $("#bcircle-1", root).css('display', 'inline');
            break;
        case 3:
            $("#line-4", root).css('stroke', '#ef7419');
            $("#circle-2", root).css('stroke', '#ef7419');
            $("#bcircle-2", root).css('display', 'inline');
            break;
        case 4:
            $("#line-5", root).css('stroke', '#32ff15');
            $("#circle-3", root).css('stroke', '#32ff15');
            $("#bcircle-3", root).css('display', 'inline');
            break;
        default:
            break;
    }
}

function strokew(min, max, coeff) {
    return (max-min)*coeff+min;

}

function getdatachart(id, url, chart, options, subscribe, token)
{
     achart = $.ajax(
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
                if (id < 3)
                {
                    $("#c_" + id).text("Смена " + data[1]);
                    $("#s_" + id).text("Смена " + data[1]);
                    data = data[0];
                }
                drawchart(id, chart, options, data);
                drawstattable(id, chart, data);
                if(subscribe) {
                    tmstat[id] = window.setTimeout(function () {
                        getdatachart(id, url, chart, options, subscribe, token);
                    }, 120000);
                }
            },
            error: function() {
                tmstat[id] = window.setTimeout(function () {
                    getdatachart(id, url, chart, options, subscribe, token);
                }, 120000);
            }
        });
}

function drawchart(id, chart, options, data) {
    options['yaxes'][0]['min'] = 0.0;
    options['yaxes'][0]['max'] = 24.5;
    if(id < 3)
    {
        options['yaxes'][0]['min'] = 0.0;
        options['yaxes'][0]['max'] = 8.5;
    }
    $.plot("#" + chart, [ data[0], data[1], data[2],
        data[3], data[4], data[5]], options);
}

function drawinfo(data, root)
{
    $("#cam").css('background-image', 'url(data:image/jpeg;base64,' + data['img'] + ')');
    $("#cam-label").text("Дата " + data['tstamp']);
    if (data['stop'] > 0.95 && data['snnclass'] !== 1) {
        $("#img").css('box-shadow', '0 0 40px #759ebf');
    }
    else
    {
        if (data['full'] < data['empty'] && data['snnclass'] !== 1)
        {
            $("#img").css('box-shadow', '0 0 25px 2px #666d6e');
        }
        else {
            //    if (data['idnext'] != null) {
            switch (data['snnclass']) {
                case 0:
                    $("#img").css('box-shadow', '0 0 25px 2px #666d6e');
                    break;
                case 1:
                    $("#img").css('box-shadow', '0 0 25px 2px #f20855');
                    break;
                case 2:
                    $("#img").css('box-shadow', '0 0 25px 2px #ff0f3c');
                    break;
                case 3:
                    $("#img").css('box-shadow', '0 0 25px 2px #ef7419');
                    break;
                case 4:
                    $("#img").css('box-shadow', '0 0 25px 2px #32ff15');
                    break;
            }
            //   }
            //   else
            //   {
            //        $("#img").css('box-shadow', '0 0 25px 2px #666d6e');
            //    }
        }
    }
    drawdata(data, root)
}

function drawstattable(id, chart, data) {
    var ch = chart.split('_');
    for (var i = 0; i < data.length; i++) {
        var a = data[i][0];
        if(a[1] !== null && a[1] !== 0.0)
          $("#" + ch[0] + "_" + id + "_" + i).text((a[1]).toFixed(2));
        else
          $("#" + ch[0] + "_" + id + "_" + i).text("-");
    }
}

function getDays() {
    var today = new Date();
    var result = new Date(today);
    result.setDate(result.getDate() - 1);
    var days = result.getDate();
    var month = result.getMonth() + 1;
    month = (month<10?'0':'') + month;
    var years = result.getFullYear();
  return days + '.' + month + '.' + years;
}

function gestatdata(url, st, en, token, options) {
    $.ajax(
        {
            url: url,
            data: {
                st: st, en: en, 'csrfmiddlewaretoken': token
            },
            timeout: 100000,
            type: 'POST',
            beforeSend: function () {
                $("#wait").show();
            },
            success: function (data) {
                $("#wait").hide();
               setstat(data, options);
            },
            error: function() {
                 $("#wait").hide();
            }
        });
}

function setstat(data, options)
{
  for (var i = 0; i < data.length && i < 4; i++) {
      var chart = 'ch_';
      if (i < 3) {
          chart += i;
      }
      else {
          chart += 'all';
      }
      var tdata = data[i];
      drawstattable(i, chart, tdata);
      options['yaxes'][0]['min'] = 0.0;
      options['yaxes'][0]['max'] = data[4][0][1];
      if (i < 3) {
          options['yaxes'][0]['min'] = 0.0;
          options['yaxes'][0]['max'] = data[4][0][0];
      }
      $.plot("#" + chart, [tdata[0], tdata[1], tdata[2],
          tdata[3], tdata[4], tdata[5]], options);
  }
}