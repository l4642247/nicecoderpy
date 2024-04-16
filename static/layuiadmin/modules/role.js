/** layuiAdmin.std-v1.1.0 LPPL License By http://www.layui.com/admin/ */
;layui.define(["table", "form", 'util', 'HttpRequest'], function (e) {
    var t = layui.$, i = layui.table , util = layui.util, HttpRequest = layui.HttpRequest;
    i.render({
        elem: "#LAY-user-back-role",
        url: "/role/page",
        cols: [[
            {type: 'numbers', width: 80, title: "ID"},
            {field: "code", title: "编码"},
            {field: "name", title: "角色名"},
            {field: "createTime",title: "创建时间", templet: function (d) {return util.toDateString(d.createTime);}},
            {title: "操作", width: 150, align: "center", fixed: "right", toolbar: "#table-option"}]],
        page: true,
        text: "对不起，加载出现异常！"
    }), i.on("tool(LAY-user-back-role)", function (e) {
        if ("del" === e.event) layer.confirm("确定删除此角色？", function (t) {
            var httpRequest = new HttpRequest("/role/delete/"+e.data.id, 'delete', function (data) {
                if(0 == data.code){
                    e.del(), layer.close(t)
                }else{
                    layer.msg(data.msg, {icon: 5})
                }
            });
            httpRequest.start(true);
        }); else if ("edit" === e.event) {
            layer.open({
                type: 2,
                title: "编辑角色",
                content: "roleform?id=" + e.data.id,
                area: ["700px", "500px"],
                btn: ["确定", "取消"],
                yes: function (e, t) {
                    var l = window["layui-layer-iframe" + e],
                        r = t.find("iframe").contents().find("#LAY-user-role-submit");
                    l.layui.form.on("submit(LAY-user-role-submit)", function (t) {
                        var httpRequest = new HttpRequest("/role/save", 'post', function (data) {
                            i.reload("LAY-user-back-role");
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
    }), e("role", {})
});