/** layuiAdmin.std-v1.1.0 LPPL License By http://www.layui.com/admin/ */
;layui.define(function (e) {
    var a=layui.admin;
    layui.use(["admin", "carousel"], function () {
        var e = layui.$, a = (layui.admin, layui.carousel), l = layui.element, t = layui.device();
        e(".layadmin-carousel").each(function () {
            var l = e(this);
            a.render({
                elem: this,
                width: "100%",
                arrow: "none",
                interval: l.data("interval"),
                autoplay: l.data("autoplay") === !0,
                trigger: t.ios || t.android ? "click" : "hover",
                anim: l.data("anim")
            })
        }), l.render("progress")
    }), layui.use(["carousel", "echarts"], function () {
        var $ = layui.$ ;
        $.ajax({
            type: "GET",
            url: "/order/echartsLineData",
            success: function(data){
                var e = layui.$, a = (layui.carousel, layui.echarts), l = [], t = [{
                    tooltip: {trigger: "axis"},
                    calculable: !0,
                    legend: {data: ["会员量", "订单量", "消费额"]},
                    xAxis: [{
                        type: "category",
                        data: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
                    }],
                    yAxis: [{type: "value", name: "会员/订单量", axisLabel: {formatter: "{value} 个"}},
                        {
                            type: "value",
                            name: "消费额",
                            axisLabel: {formatter: "{value} 元"}
                        }],
                    series: [{
                        name: "会员量",
                        type: "line",
                        data: data.data.memberArr
                    }, {
                        name: "订单量",
                        type: "line",
                        data: data.data.orderNumArr
                    }, {
                        name: "消费额",
                        type: "line",
                        yAxisIndex: 1,
                        data: data.data.amountArr
                    }]
                }], i = e("#LAY-index-pagetwo").children("div"), n = function (e) {
                    l[e] = a.init(i[e], layui.echartsTheme), l[e].setOption(t[e]), window.onresize = l[e].resize
                };
                i[0] && n(0)
            }
        });


    }), layui.use(["carousel", "echarts"], function () {
        var $ = layui.$ ;
        $.ajax({
            type: "GET",
            url: "/order/echartsPieData",
            success: function(data){
                var e = layui.$, a = (layui.carousel, layui.echarts), l = [], t = [{
                    title: {
                        text: '营业额（月）',
                        x: 'left',
                        textStyle:{
                            fontSize:14,
                            color:'#333',
                            fontFamily:'Helvetica Neue,Helvetica,PingFang SC,Tahoma,Arial,sans-serif'

                        }
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c}元 ({d}%)"
                    },
                    stillShowZeroSum: false,
                    series: [
                        {
                            name: '金额',
                            type: 'pie',
                            radius: '50%',
                            center: ['50%', '50%'],
                            data: data.data
                        }
                    ]
                }], i = e("#LAY-index-pagethree").children("div"), n = function (e) {
                    l[e] = a.init(i[e], layui.echartsTheme), l[e].setOption(t[e]), window.onresize = l[e].resize
                };
                i[0] && n(0)
            }
        });

    }), layui.use("table", function () {
        var e = (layui.$, layui.table);
        e.render({
            elem: "#LAY-index-prograss",
            url: layui.setter.base + "json/console/prograss.js",
            cols: [[{type: "checkbox", fixed: "left"}, {field: "prograss", title: "任务"}, {
                field: "time",
                title: "所需时间"
            }, {
                field: "complete", title: "完成情况", templet: function (e) {
                    return "已完成" == e.complete ? '<del style="color: #5FB878;">' + e.complete + "</del>" : "进行中" == e.complete ? '<span style="color: #FFB800;">' + e.complete + "</span>" : '<span style="color: #FF5722;">' + e.complete + "</span>"
                }
            }]],
            skin: "line"
        })
    }), a.events.replyNote = function (e) {
        var a = e.data("id");
        layer.prompt({title: "回复留言 ID:" + a, formType: 2}, function (e, a) {
            layer.msg("得到：" + e), layer.close(a)
        })
    }, e("sample", {})
});