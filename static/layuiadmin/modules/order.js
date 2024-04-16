/** layuiAdmin.std-v1.1.0 LPPL License By http://www.layui.com/admin/ */
;layui.define(["table", "form", 'util', 'HttpRequest'], function (e) {
    var t = layui.$, i = layui.table , util = layui.util, HttpRequest = layui.HttpRequest;
    i.render({
        elem: "#LAY-order",
        url: "/order/page",
        cols: [[
            {type: 'numbers', width: 80, title: "ID"},
            {field: "cardNo", title: "卡号", templet: function (d) {return d.cardNo == null ? "-" : d.cardNo}},
            {field: "memberName", title: "会员名", templet: function (d) {return d.memberName == null ? "-" : d.memberName}},
            {field: "barberName", title: "用户名"},
            {field: "type", title: "类型" , width: 150, align:'center'
                ,templet: function (d) {return d.type == '1'?"<span class=\"layui-badge\">充值</span>":"<span class=\"layui-badge layui-bg-green\">消费</span>";}},
            {field: "amount", title: "金额"},
            {field: "status", title: "状态" ,templet: function (d) {return d.status == '1'?"已完成":"取消";}},
            {field: "creatorName", width:100, title: "操作人"},
            {field: "createTime", width: 170,title: "创建时间", templet: function (d) {
                    return util.toDateString(d.createTime);}},
            ]],
        page: true,
        text: "对不起，加载出现异常！"
    }), e("order", {})
});