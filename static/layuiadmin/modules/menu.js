/** layuiAdmin.std-v1.1.0 LPPL License By http://www.layui.com/admin/ */
;layui.define(["table", "form", 'util', 'HttpRequest'], function (e) {
    var t = layui.$, i = layui.table , util = layui.util, HttpRequest = layui.HttpRequest;

    i.render({
        elem: "#LAY-menu-manage",
        url: "/menu/page",
        cols: [[
            {type: 'numbers', width: 80, title: "ID"},
            {field: "name", title: "菜单名" },
            {field: "css", width: 60, align:"center", title: "图标", templet: function (d) {return d.css == '' ? "-":'<i class="layui-icon ' + d.css + '"></i> '}},
            {field: "href", title: "路径", templet: function (d) {return d.href == '' ? "-":d.href}},
            {field: "sort", width: 60, title: "排序"},
            {field: "type", width: 60,title: "类型", align:"center", templet: function (d) {return d.type == '1'? "菜单":"页面";}},
            // {field: "status", title: "状态", align:"center",templet: function (d) { return d.status == '1'?"启用":"禁用";}},
            {field: "createTime", title: "添加时间", templet: function (d) {return util.toDateString(d.createTime);}},
            {title: "操作", width: 150, align: "center", fixed: "right", toolbar: "#table-option"}]],
        page: !0,
        limit: 30,
        height: "full-220",
        text: "对不起，加载出现异常！"
    }), i.on("tool(LAY-menu-manage)", function (e) {
        if ("del" === e.event) layer.confirm("确定删除此菜单？", function (t) {
            var httpRequest = new HttpRequest("/menu/delete/"+e.data.id, 'delete', function (data) {
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
                title: "编辑菜单信息",
                content: "menuform?id=" + e.data.id,
                area: ["800px", "550px"],
                btn: ["确定", "取消"],
                yes: function (e, t) {
                    var l = window["layui-layer-iframe" + e],
                        r = t.find("iframe").contents().find("#LAY-menu-submit");
                    l.layui.form.on("submit(LAY-menu-submit)", function (t) {
                        var httpRequest = new HttpRequest("/menu/save", 'post', function (data) {
                            i.reload("LAY-menu-manage");
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
    }), e("menu", {})
});