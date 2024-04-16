/** layuiAdmin.std-v1.1.0 LPPL License By http://www.layui.com/admin/ */
;layui.define(["table", "form", 'util', 'HttpRequest'], function (e) {
    var t = layui.$, i = layui.table , util = layui.util, HttpRequest = layui.HttpRequest , $ = layui.$;

    i.render({
        elem: "#LAY-user-manage",
        url: "/company/page",
        cols: [[
            {type: 'numbers', width: 50, title: "ID"},
            {field: "name", title: "企业名称" },
            {field: "requirment", title: "职位需求"},
            {field: "telephone", title: "电话号码"},
            {field: "email", title: "电子邮箱"},
            {title: "操作", width: 180, align: "center", fixed: "right", toolbar: "#table-option"}]],
        page: !0,
        limit: 30,
        height: "full-220",
        text: "对不起，加载出现异常！"
    }), i.on("tool(LAY-user-manage)", function (e) {
        if ("audit" === e.event) layer.confirm("确定审核此用户？", function (t) {
            $.ajax({
                type: "put",
                data: {"id": e.data.userId, "status": 1},
                url: "/user/updateStatus/",
                success: function(data){
                    layer.msg(data.msg, {icon: 1})
                }
            });
        }); else if ("detail" === e.event) {
            layer.open({
                type: 2,
                title: "企业用户信息",
                content: "/user/companydetail?id=" + e.data.id,
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
    }), e("company", {})
});