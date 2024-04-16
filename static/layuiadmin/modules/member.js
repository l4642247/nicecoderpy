/** layuiAdmin.std-v1.1.0 LPPL License By http://www.layui.com/admin/ */
;layui.define(["table", "form", 'util', 'HttpRequest'], function (e) {
    var t = layui.$, i = layui.table , util = layui.util, HttpRequest = layui.HttpRequest;
    i.render({
        elem: "#LAY-user-member",
        url: "/member/page",
        cols: [[
            {type: "checkbox", fixed: "left"},
            {type: 'numbers', width: 80, title: "ID"},
            {field: "cardNo", width:120, title: "卡号", minWidth: 100},
            {field: "idCard", width:120, title: "身份证号", minWidth: 100},
            {field: "name", title: "姓名", width: 80},
            {field: "sex", title: "性别", align:"center", templet: function (d) {return d.sex == '1' ? "男":"女";}},
            {field: "phone", width:120, title: "联系电话"},
            {field: "balance", width:80, title: "余额"},
            {field: "status", title: "状态", align:"center", templet: function (d) {return d.status == '1'? "正常":"删除";}},
            {field: "createTime", width:170, title: "添加时间",templet: function (d) {return util.toDateString(d.createTime);}},
            {title: "操作", width: 300, align: "center", fixed: "right", toolbar: "#table-option"}]],
        page: !0,
        limit: 30,
        height: "full-220",
        text: "对不起，加载出现异常！"
    }), i.on("tool(LAY-user-member)", function (e) {
        if ("del" === e.event) layer.confirm("确定删除此用户？", function (t) {
            var httpRequest = new HttpRequest("/member/delete/"+e.data.id, 'delete', function (data) {
                if(0 == data.code){
                    e.del(), layer.close(t)
                }else{
                    layer.msg(data.msg, {icon: 5})
                }
            });
            httpRequest.start(true);
        });
        else if ("edit" === e.event) {
            layer.open({
                type: 2,
                title: "编辑用户信息",
                content: "memberform?id=" + e.data.id,
                area: ["600px", "450px"],
                btn: ["确定", "取消"],
                yes: function (e, t) {
                    var l = window["layui-layer-iframe" + e],
                        r = t.find("iframe").contents().find("#LAY-user-member-submit");
                    l.layui.form.on("submit(LAY-user-member-submit)", function (t) {
                        var httpRequest = new HttpRequest("/member/save", 'post', function (data) {
                            i.reload("LAY-user-member");
                            layer.close(e)
                        });
                        httpRequest.set(t.field);
                        httpRequest.start(true);
                    }), r.trigger("click")
                },
                success: function (e, t) {
                }
            })
        }
        else if ("recharge" === e.event) {
            layer.open({
                type: 2,
                title: "充值",
                content: "rechargeform?memberId=" + e.data.id,
                area: ["600px", "450px"],
                btn: ["确定", "取消"],
                yes: function (e, t) {
                    var l = window["layui-layer-iframe" + e],
                        r = t.find("iframe").contents().find("#LAY-order-recharge-submit");
                    l.layui.form.on("submit(LAY-order-recharge-submit)", function (t) {
                        var httpRequest = new HttpRequest("/member/recharge", 'post', function (data) {
                            i.reload("LAY-user-member");
                            layer.close(e)
                        });
                        httpRequest.set(t.field);
                        httpRequest.start(true);
                    }), r.trigger("click")
                },
                success: function (e, t) {
                }
            })
        }
        else if ("expense" === e.event) {
            layer.open({
                type: 2,
                title: "消费",
                content: "expenseform?memberId=" + e.data.id,
                area: ["600px", "450px"],
                btn: ["确定", "取消"],
                yes: function (e, t) {
                    var l = window["layui-layer-iframe" + e],
                        r = t.find("iframe").contents().find("#LAY-order-expense-submit");
                    l.layui.form.on("submit(LAY-order-expense-submit)", function (t) {
                        var httpRequest = new HttpRequest("/member/expense", 'post', function (data) {
                            if(data.code == 0){
                                i.reload("LAY-user-member");
                                layer.close(e)
                            }else{
                                layer.msg(data.msg, {icon: 5})
                            }
                        });
                        httpRequest.set(t.field);
                        httpRequest.start(true);
                    }), r.trigger("click")
                },
                success: function (e, t) {
                }
            })
        }}),e("member", {})
});