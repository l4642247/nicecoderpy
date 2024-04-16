/** layuiAdmin.std-v1.1.0 LPPL License By http://www.layui.com/admin/ */
;layui.define(["table", "form", 'util', 'HttpRequest'], function (e) {
    var t = layui.$, i = layui.table , util = layui.util, HttpRequest = layui.HttpRequest, $ = layui.$;

    i.render({
        elem: "#LAY-user-manage",
        url: "/candidate/page",
        cols: [[
            {type: 'numbers', width: 50, title: "ID"},
            {field: "name",  width: 100, title: "姓名" },
            {field: "sex", width: 60, title: "性别", align:"center", templet: function (d) {return d.sex == '1'?"男":"女";}},
            {field: "school", title: "毕业学校"},
            {field: "major", title: "专业类别", templet:'#switchTpl2'},
            {field: "salary", title: "期望薪资", templet:'#switchTpl'},
            {field: "telephone", title: "手机号"},
            {field: "email", title: "邮箱"},
            {title: "操作", width: 250, align: "center", fixed: "right", toolbar: "#table-option"}]],
        page: !0,
        limit: 30,
        height: "full-220",
        text: "对不起，加载出现异常！"
    }), i.on("tool(LAY-user-manage)", function (e) {
        if ("agree" === e.event) layer.confirm("通过此用户的申请？", function (t) {
            $.ajax({
                type: "put",
                url: "/applylog/agree/" + e.data.userId,
                success: function(data){
                    layer.msg(data.msg, {icon: 1})
                }
            });
        });
        else if ("reject" === e.event) layer.confirm("拒绝此用户的申请？", function (t) {
            $.ajax({
                type: "put",
                url: "/applylog/reject/" + e.data.userId,
                success: function(data){
                    layer.msg(data.msg, {icon: 1})
                }
            });
        });
        else if ("detail" === e.event) {
            layer.open({
                type: 2,
                title: "个人用户信息",
                content: "/user/candidatedetail?id=" + e.data.id,
                area: ["800px", "550px"],
                btn: ["确定", "取消"],
                yes: function (e, t) {
                    var l = window["layui-layer-iframe" + e],
                        r = t.find("iframe").contents().find("#LAY-user-submit");
                    l.layui.form.on("submit(LAY-user-submit)", function (t) {
                        var httpRequest = new HttpRequest("/user/update", 'post', function (data) {
                            i.reload("LAY-user-manage");
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
    }), e("candidaterepo", {})
});